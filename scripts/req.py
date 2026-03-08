from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from typing import Any

import requests

HOME_RECOMMEND_URL = "https://api.bilibili.com/x/web-interface/wbi/index/top/feed/rcmd"
RELATED_URL = "https://api.bilibili.com/x/web-interface/archive/related"
FAVORITE_URL = "https://api.bilibili.com/medialist/gateway/coll/resource/deal"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


class BiliApiError(RuntimeError):
    def __init__(self, code: int, message: str):
        super().__init__(f"Bilibili API error {code}: {message}")
        self.code = code
        self.message = message


@dataclass
class BiliConfig:
    sessdata: str
    favorite_folder_id: int
    user_agent: str = DEFAULT_USER_AGENT

    @classmethod
    def from_env(cls) -> "BiliConfig":
        sessdata = os.environ.get("BILI_SESSDATA", "").strip()
        if not sessdata:
            raise ValueError("缺少环境变量 BILI_SESSDATA")

        favorite_folder_id_raw = os.environ.get("BILI_FAVORITE_FOLDER_ID", "").strip()
        if not favorite_folder_id_raw:
            raise ValueError("缺少环境变量 BILI_FAVORITE_FOLDER_ID")
        try:
            favorite_folder_id = int(favorite_folder_id_raw)
        except ValueError as exc:
            raise ValueError("环境变量 BILI_FAVORITE_FOLDER_ID 必须是整数") from exc

        return cls(
            sessdata=sessdata,
            favorite_folder_id=favorite_folder_id,
        )


@dataclass
class VideoSummary:
    aid: int
    bvid: str
    title: str
    owner_name: str
    owner_mid: int
    duration_seconds: int
    view_count: int
    like_count: int
    danmaku_count: int
    reason: str | None
    uri: str

    @property
    def duration_text(self) -> str:
        minutes, seconds = divmod(self.duration_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["duration_text"] = self.duration_text
        return payload


class BiliClient:
    def __init__(self, config: BiliConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": config.user_agent,
                "Referer": "https://www.bilibili.com",
            }
        )

    @property
    def cookies(self) -> dict[str, str]:
        return {"SESSDATA": self.config.sessdata}

    def _request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        response = self.session.request(method, url, cookies=self.cookies, timeout=20, **kwargs)
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 0:
            raise BiliApiError(payload.get("code", -1), payload.get("message", "unknown error"))
        return payload

    def get_home_recommendations(self, limit: int = 12, fresh_idx: int = 1) -> list[VideoSummary]:
        payload = self._request(
            "GET",
            HOME_RECOMMEND_URL,
            params={"ps": limit, "fresh_type": 3, "fresh_idx": fresh_idx},
        )
        items = payload.get("data", {}).get("item", [])
        return [self._video_summary_from_item(item) for item in items if item.get("bvid")]

    def get_related_videos(self, *, bvid: str | None = None, aid: int | None = None) -> list[VideoSummary]:
        if not bvid and not aid:
            raise ValueError("bvid 和 aid 至少需要提供一个")
        params: dict[str, Any] = {}
        if bvid:
            params["bvid"] = bvid
        if aid:
            params["aid"] = aid
        payload = self._request("GET", RELATED_URL, params=params)
        return [self._video_summary_from_item(item) for item in payload.get("data", []) if item.get("bvid")]

    def add_to_favorites(self, aid: int) -> dict[str, Any]:
        payload = self._request(
            "POST",
            FAVORITE_URL,
            data={
                "rid": aid,
                "type": 2,
                "add_media_ids": self.config.favorite_folder_id,
                "csrf": "0",
            },
        )
        return payload

    @staticmethod
    def _video_summary_from_item(item: dict[str, Any]) -> VideoSummary:
        owner = item.get("owner") or {}
        stat = item.get("stat") or {}
        reason_value = item.get("rcmd_reason")
        if isinstance(reason_value, dict):
            reason = reason_value.get("content")
        elif isinstance(reason_value, str) and reason_value:
            reason = reason_value
        else:
            reason = None
        aid = item.get("id") or item.get("aid") or stat.get("aid") or 0
        bvid = item.get("bvid", "")
        uri = item.get("uri") or (f"https://www.bilibili.com/video/{bvid}" if bvid else "")
        return VideoSummary(
            aid=aid,
            bvid=bvid,
            title=item.get("title", ""),
            owner_name=owner.get("name", ""),
            owner_mid=owner.get("mid", 0),
            duration_seconds=item.get("duration", 0),
            view_count=stat.get("view", 0),
            like_count=stat.get("like", 0),
            danmaku_count=stat.get("danmaku", 0),
            reason=reason,
            uri=uri,
        )


def load_config() -> BiliConfig:
    return BiliConfig.from_env()


def run_recommend(client: BiliClient, fresh_idx: int, limit: int) -> None:
    videos = client.get_home_recommendations(limit=limit, fresh_idx=fresh_idx)
    output = [video.to_dict() for video in videos]
    print(json.dumps(output, ensure_ascii=False, indent=2))


def run_related(client: BiliClient, bvid: str | None, aid: int | None) -> None:
    videos = client.get_related_videos(bvid=bvid, aid=aid)
    output = [video.to_dict() for video in videos]
    print(json.dumps(output, ensure_ascii=False, indent=2))


def run_favorite(client: BiliClient, aid: int) -> None:
    result = client.add_to_favorites(aid=aid)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bilibili 推荐与收藏测试脚本")
    subparsers = parser.add_subparsers(dest="command", required=True)

    recommend_parser = subparsers.add_parser("recommend", help="获取首页推荐视频")
    recommend_parser.add_argument("--fresh-idx", type=int, default=1)
    recommend_parser.add_argument("--limit", type=int, default=12)

    related_parser = subparsers.add_parser("related", help="获取单条视频的相关推荐")
    related_parser.add_argument("--bvid")
    related_parser.add_argument("--aid", type=int)

    favorite_parser = subparsers.add_parser("favorite", help="收藏视频到固定收藏夹")
    favorite_parser.add_argument("--aid", type=int, required=True)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    client = BiliClient(load_config())

    try:
        if args.command == "recommend":
            run_recommend(client, fresh_idx=args.fresh_idx, limit=args.limit)
        elif args.command == "related":
            run_related(client, bvid=args.bvid, aid=args.aid)
        elif args.command == "favorite":
            run_favorite(client, aid=args.aid)
        return 0
    except (BiliApiError, requests.RequestException, ValueError) as exc:
        print(f"请求失败: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
