#### 获取首页视频推荐

> https://api.bilibili.com/x/web-interface/wbi/index/top/feed/rcmd

请求方式：GET

认证方式：Cookie（SESSDATA）

最多获取30条推荐视频,直播及推荐边栏。

##### url参数：

| 参数名        | 类型 | 内容                   | 必要性 | 备注                                                  |
| ------------- | ---- | ---------------------- | ------ | ----------------------------------------------------- |
| fresh_type    | num  | 相关性                 | 非必要 | 默认为 4 值越大推荐内容越相关                         |
| ps            | num  | 单页返回的记录条数     | 非必要 | 默认为 12, 留空即最大值为 30                          |
| fresh_idx     | num  | 当前翻页号             | 非必要 | 以 1 开始                                             |
| fresh_idx_1h  | num  | 当前翻页号(一小时前?)  | 非必要 | 以 1 开始, 默认与 fresh_idx 内容相同                  |
| brush         | num  | 刷子?                  | 非必要 | 以 1 开始, 默认与 fresh_idx 内容相同                  |
| fetch_row     | num  | 本次抓取的最后一行行号 | 非必要 | 1 递归加上本次抓取总行数                              |
| web_location  | num  | 网页位置               | 非必要 | 主页为 1430650                                        |
| y_num         | num  | 普通列数               | 非必要 | 一行中视频,直播及广告数                               |
| last_y_num    | num  | 总列数                 | 非必要 | 普通列数 + 边栏列数                                   |
| feed_version  | str  | V8                     | 非必要 | 作用尚不明确                                          |
| homepage_ver  | num  | 1                      | 非必要 | 首页版本                                              |
| screen        | str  | 浏览器视口大小         | 非必要 | 水平在前垂直在后以减号分割                            |
| seo_info      | str  | 空                     | 非必要 | 作用尚不明确                                          |
| last_showlist | str  | 上次抓取的视频av号列表 | 非必要 | av与数字间用下划线分隔, 若视频UP主已关注则中间再插入n |
| uniq_id       | str  | ???                    | 非必要 | 作用尚不明确                                          |

**json回复：**

根对象：

| 字段    | 类型 | 内容     | 备注                   |
| ------- | ---- | -------- | ---------------------- |
| code    | num  | 返回值   | 0：成功 -400：请求错误 |
| message | str  | 错误信息 | 默认为0                |
| ttl     | num  | 1        |                        |
| data    | obj  |          |                        |

`data`对象：

| 字段                     | 类型  | 内容      | 备注                           |
| ------------------------ | ----- | --------- | ------------------------------ |
| business_card            | null  |           |                                |
| floor_info               | null  |           |                                |
| item                     | array | 推荐列表  |                                |
| mid                      | num   | 用户mid   | 未登录为0                      |
| preload_expose_pct       | num   | 0.5       | 用于预加载?                    |
| preload_floor_expose_pct | num   | 0.5       | 用于预加载?                    |
| side_bar_column          | array | 边栏列表? | 可参考字段 item 及对应功能文档 |
| user_feature             | null  |           |                                |

`data`对象中`item`数组中的对象:

| 字段              | 类型 | 内容               | 备注                                                         |
| ----------------- | ---- | ------------------ | ------------------------------------------------------------ |
| av_feature        | null |                    |                                                              |
| business_info     | obj  | 商业推广信息       | 无为null 对于推广内容，视频信息会在这个dict的"archive"属性下 |
| bvid              | str  | 视频bvid           |                                                              |
| cid               | num  | 稿件cid            |                                                              |
| dislike_switch    | num  | 1                  | 显示不感兴趣开关?                                            |
| dislike_switch_pc | num  | 0                  | 显示不感兴趣开关(PC)?                                        |
| duraion           | num  | 视频时长           |                                                              |
| enable_vt         | num  | 0                  | 作用尚不明确                                                 |
| goto              | num  | 目标类型           | av: 视频 ogv: 边栏 live: 直播                                |
| duraion           | num  | 视频时长           |                                                              |
| id                | num  | 视频aid / 直播间id |                                                              |
| is_followed       | num  | 已关注             | 0: 未关注 1: 已关注                                          |
| is_stock          | num  | 0                  | 作用尚不明确                                                 |
| ogv_info          | null |                    |                                                              |
| owner             | obj  | UP主               |                                                              |
| pic               | str  | 封面               |                                                              |
| pic_4_3           | str  | 封面(4:3)          |                                                              |
| pos               | num  | 0                  | 位置?                                                        |
| pubdate           | num  | 发布时间           |                                                              |
| rcmd_reason       | obj  | 推荐理由           | 直播等为null                                                 |
| room_info         | obj  | 直播间信息         | 普通视频等为null, 参见[直播](https://sessionhu.github.io/bilibili-API-collect/docs/live) |
| show_info         | num  | 展示信息           | 1: 普通视频 0: 直播                                          |
| stat              | obj  | 视频状态信息       | 直播等为null, 参见[视频基本信息](https://sessionhu.github.io/bilibili-API-collect/docs/video/info.html) |
| title             | str  | 标题               |                                                              |
| track_id          | str  | 跟踪标识?          |                                                              |
| uri               | str  | 目标页 URI         |                                                              |
| vt_display        | str  | 空                 | 作用尚不明确                                                 |

`item`数组中的对象中的`owner`对象:

| 字段 | 类型 | 内容    | 备注 |
| ---- | ---- | ------- | ---- |
| face | str  | 头像URL |      |
| mid  | num  | UP主mid |      |
| name | str  | UP昵称  |      |

`item`数组中的对象中的`rcmd_reason`对象:

| 字段        | 类型 | 内容     | 备注                        |
| ----------- | ---- | -------- | --------------------------- |
| reason_type | num  | 原因类型 | 0: 无 1: 已关注 3: 高点赞量 |
| content     | str  | 原因描述 | 当 reason_type 为 3 时存在  |

##### 示例：

```bash
curl -G 'https://api.bilibili.com/x/web-interface/wbi/index/top/feed/rcmd' \
--data-urlencode 'fresh_type=4' \
--data-urlencode 'ps=12' \
--data-urlencode 'fresh_idx=5' \
--data-urlencode 'fresh_idx_1h=5' \
--data-urlencode 'fetch_row=16'
```



#### 获取单视频的推荐列表

> https://api.bilibili.com/x/web-interface/archive/related

请求方式：GET

最多获取40条推荐视频。

**url参数：**

| 参数名 | 类型 | 内容     | 必要性       | 备注               |
| ------ | ---- | -------- | ------------ | ------------------ |
| aid    | num  | 稿件avid | 必要（可选） | avid与bvid任选一个 |
| bvid   | str  | 稿件bvid | 必要（可选） | avid与bvid任选一个 |

**json回复：**

根对象：

| 字段    | 类型  | 内容     | 备注                   |
| ------- | ----- | -------- | ---------------------- |
| code    | num   | 返回值   | 0：成功 -400：请求错误 |
| message | str   | 错误信息 | 默认为0                |
| ttl     | num   | 1        |                        |
| data    | array | 推荐列表 |                        |

`data`数组：

| 项   | 类型 | 内容          | 备注 |
| ---- | ---- | ------------- | ---- |
| 0    | obj  | 推荐视频1     |      |
| n    | obj  | 推荐视频(n+1) |      |
| ……   | obj  | ……            | ……   |
| 39   | obj  | 推荐视频40    |      |

##### **示例：**

查询视频`av7`/`BV1xx411c7m9`的推荐视频列表：

```bash
# avid方式
curl -G 'https://api.bilibili.com/x/web-interface/archive/related' \
--data-urlencode 'aid=7'

# bvid方式
curl -G 'https://api.bilibili.com/x/web-interface/archive/related' \
--data-urlencode 'bvid=BV1xx411c7m9'
```





#### 收藏视频

> https://api.bilibili.com/medialist/gateway/coll/resource/deal

请求方式：POST

认证方式：Cookie(SESSDATA)

鉴权方式需要验证referer为 `.bilibili.com`域名下

##### **正文参数（ application/x-www-form-urlencoded ）：**

| 参数名        | 类型 | 内容                      | 必要性          | 备注                           |
| ------------- | ---- | ------------------------- | --------------- | ------------------------------ |
| rid           | num  | 稿件 avid                 | 必要            |                                |
| type          | num  | 必须为2                   | 必要            |                                |
| add_media_ids | nums | 需要加入的收藏夹 mlid     | 必要(可选)      | 同时添加多个，用`,`（%2C）分隔 |
| del_media_ids | nums | 需要取消的收藏夹 mlid     | 必要(可选)      | 同时取消多个，用`,`（%2C）分隔 |
| csrf          | str  | CSRF Token（位于 Cookie） | Cookie 方式必要 |                                |

##### **json回复：**

根对象：

| 字段    | 类型 | 内容     | 备注                                                         |
| ------- | ---- | -------- | ------------------------------------------------------------ |
| code    | num  | 返回值   | 0：成功 -101：账号未登录 -111：csrf校验失败 -400：请求错误 -403：访问权限不足 10003：不存在该稿件 11010: 您访问的内容不存在 11201：已经收藏过了 11202：已经取消收藏了 11203：达到收藏上限 72010017：参数错误 |
| message | str  | 错误信息 | 正确为success                                                |
| data    | obj  | 信息本体 |                                                              |

`data`对象：

| 字段   | 类型 | 内容                 | 备注               |
| ------ | ---- | -------------------- | ------------------ |
| prompt | bool | 是否为未关注用户收藏 | false：否 true：是 |

##### 示例：

将视频`av49166435`添加到收藏夹`49166435`中

```bash
curl 'https://api.bilibili.com/medialist/gateway/coll/resource/deal' \
--data-urlencode 'rid=90671873' \
--data-urlencode 'type=2' \
--data-urlencode 'add_media_ids=49166435' \
--data-urlencode 'del_media_ids=' \
--data-urlencode 'csrf=xxx' \
-b 'SESSDATA=xxx' \
-e 'https://www.bilibili.com'
```

