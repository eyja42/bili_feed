---
name: bili_feed
description: 'For bilibili-related tasks. Use when fetching bilibili homepage recommendations, fetch related videos for a specific BV/AV 视频号, add video to favorites, capture real JSON samples.'
argument-hint: ' bilibili | AV | BV | 收藏 '
metadata: 
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["python"],
            "env": ["BILI_SESSDATA", "BILI_FAVORITE_FOLDER_ID"],
            "env_docs":
              {
                "BILI_SESSDATA": "Bilibili 登录 Cookie 中的 SESSDATA 字段。详见 README.md -> 获取环境变量配置（必填） -> BILI_SESSDATA。",
                "BILI_FAVORITE_FOLDER_ID": "目标收藏夹 ID（整数）。详见 README.md -> 获取环境变量配置（必填） -> BILI_FAVORITE_FOLDER_ID。"
              }
          },
        "setup_guide": "If BILI_SESSDATA or BILI_FAVORITE_FOLDER_ID is missing, ask user to follow README.md -> 获取环境变量配置（必填）, then verify with echo commands and rerun the original command.",
        "docs": ["README.md"]
      }
  }
---



## 功能

用于带鉴权访问 B 站接口，执行若干用户相关操作。具体包括：

- 获取首页推荐视频
- 获取某个视频的相关推荐列表
- 将视频添加到收藏夹

## 关键文件

- [scripts/req.py](./scripts/req.py): 执行具体逻辑的脚本，详细传入参数见下方操作流程。
- [samples](./samples): 只读的返回样例示范以及request的api说明。**正常情况下不要读取，只在 Skill 返回异常时用于判断参数问题或 API 变更。**
- [references/data-contract.md](./references/data-contract.md): 结构化输出字段约定

## 操作流程

### 0. 先确认环境变量是否已配置

```powershell
echo $env:BILI_SESSDATA
echo $env:BILI_FAVORITE_FOLDER_ID
```

如果为空，请按 `README.md` 的“获取环境变量配置（必填）”完成配置。

### 1. 获取首页推荐

运行命令：

```powershell
python scripts/req.py recommend --fresh-idx 1 --limit 12
```

输出内容：

- 结构化后的推荐视频列表
- 直接打印 JSON 结果（不写入 samples）

### 2. 获取相关推荐

下面的例子可以获取视频BV1PTfnBLECK的相关推荐：

```powershell
python scripts/req.py related --bvid BV1PTfnBLECK
```

也可以改用 `--aid`。

### 3. 收藏特定视频

下面的例子会把视频收藏到环境变量 `BILI_FAVORITE_FOLDER_ID` 指定的固定收藏夹：

```powershell
python scripts/req.py favorite --aid 116166567660430
```