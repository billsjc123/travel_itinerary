# 旅行计划集 · travel_itinerary

把每一段旅程的行程文档都放在这里，主页 `index.html` 会自动列出所有行程，点进去看详情。

## 目录结构

```
travel_itinerary/
├── index.html          # 主页（自动生成，勿手改）
├── trips.json          # 行程清单（唯一数据源，加行程改这里）
├── build_index.py      # 生成器：读取 trips.json → 写 index.html
├── README.md          # 本说明
└── *.html             # 各段旅程的详情页（如 fuji-itinerary.html）
```

> 本站为 GitHub Pages 项目站，部署源设为 `main` 分支 `/ (root)`。
> 主页地址：`https://<用户名>.github.io/travel_itinerary/`

## 怎么加一段新旅程

1. **写详情页**：新建一个 HTML 文件，例如 `osaka-itinerary.html`。
   建议详情页顶部保留一个返回链接：
   `<a href="index.html">← 返回所有行程</a>`
2. **登记到清单**：打开 `trips.json`，在 `trips` 数组里加一项：

   ```json
   {
     "file": "osaka-itinerary.html",
     "title": "大阪美食之旅",
     "emoji": "🍜",
     "dates": "2026.08.10 – 08.14",
     "place": "日本 · 大阪 / 京都",
     "tags": ["美食", "逛街"],
     "blurb": "环球影城两天 + 心斋桥逛吃 + 京都一日游。",
     "updated": "2026-08-01"
   }
   ```

3. **重新生成主页**（在本目录运行）：

   ```bash
   python3 build_index.py
   ```

4. **提交推送**：

   ```bash
   git add .
   git commit -m "add osaka trip"
   git push origin main
   ```

主页会显示新卡片，点进去就是详情页。详情页里的图片请使用 base64 内嵌（不要用本地绝对路径），这样别人下载单文件也能看到图。
