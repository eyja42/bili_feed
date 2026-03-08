# Data Contract

`req.py` 不会把B站原始响应暴露给上层，而是整理成稳定的数据结构。

## 标准视频结构

```json
{
  "aid": 116175207929277,
  "bvid": "BV1UJPrzsE6P",
  "title": "示例标题",
  "owner_name": "UP 主",
  "owner_mid": 46470268,
  "duration_seconds": 374,
  "view_count": 188962,
  "like_count": 6051,
  "danmaku_count": 367,
  "reason": null,
  "uri": "https://www.bilibili.com/video/BV1UJPrzsE6P",
  "duration_text": "06:14"
}
```

## 字段来源差异

首页推荐与相关推荐的返回结构不一致，当前实现已做兼容。

### 首页推荐

- 视频 ID 字段通常是 `id`
- 链接字段通常是 `uri`
- 推荐理由通常是 `rcmd_reason.content`

### 相关推荐

- 视频 ID 字段通常是 `aid`
- 通常没有 `uri`
- 推荐理由可能是空字符串

兼容策略:

- `aid` 优先从 `id`、`aid`、`stat.aid` 依次回退
- `uri` 缺失时用 `bvid` 自动拼成 `https://www.bilibili.com/video/<bvid>`
- `reason` 同时兼容对象、字符串和空值

## 收藏接口返回

收藏接口的返回格式:

```json
{
  "code": 0,
  "data": {
    "prompt": false
  },
  "message": "success"
}
```
