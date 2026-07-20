#!/usr/bin/env python3
# 读取 trips.json，生成自包含的 index.html（数据内联，本地/Pages 均可）。
# 用法：python3 build_index.py
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
data = json.loads((ROOT / "trips.json").read_text(encoding="utf-8"))
trips_json = json.dumps(data, ensure_ascii=False)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__SITE_TITLE__</title>
<style>
  :root{
    --bg:#fafafa; --card:#fff; --border:#e0e0e0;
    --text:#2c2c2c; --muted:#666; --accent:#c0392b;
    --blue:#2980b9; --green:#27ae60; --orange:#e67e22; --purple:#8e44ad;
    --shadow:0 2px 12px rgba(0,0,0,.08); --radius:14px;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:-apple-system,"SF Pro Text","Hiragino Sans","Noto Sans SC",sans-serif;
    background:var(--bg); color:var(--text); line-height:1.7; padding:24px 20px 60px; max-width:1000px; margin:auto;}
  a{color:var(--blue);text-decoration:none}
  /* Hero */
  .hero{text-align:center; padding:46px 20px 30px;}
  .hero .emoji{font-size:54px; display:block; margin-bottom:10px;}
  .hero h1{font-size:30px; letter-spacing:.5px;}
  .hero .subtitle{font-size:15px; color:var(--muted); margin-top:8px;}
  .count{display:inline-block; margin-top:14px; font-size:12px; color:var(--muted);
    background:var(--card); border:1px solid var(--border); border-radius:999px; padding:5px 16px;}
  /* Grid */
  .grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:20px; margin-top:28px;}
  .trip-card{background:var(--card); border:1px solid var(--border); border-radius:var(--radius);
    box-shadow:var(--shadow); overflow:hidden; display:flex; flex-direction:column;
    transition:transform .15s ease, box-shadow .15s ease;}
  .trip-card:hover{transform:translateY(-4px); box-shadow:0 8px 24px rgba(0,0,0,.13);}
  .cover{height:120px; display:flex; align-items:center; justify-content:center;
    background:linear-gradient(135deg,#c0392b,#e67e22); font-size:54px;}
  .body{padding:16px 18px 20px; display:flex; flex-direction:column; flex:1;}
  .body h2{font-size:18px; font-weight:700;}
  .meta{font-size:12.5px; color:var(--muted); margin-top:4px;}
  .place{font-size:12.5px; color:var(--muted); margin-top:2px;}
  .blurb{font-size:13px; color:#444; margin-top:10px; flex:1;}
  .tags{margin-top:12px; display:flex; gap:6px; flex-wrap:wrap;}
  .tag{font-size:11px; padding:2px 10px; border-radius:99px; background:#f0f0f0; color:#555;}
  .more{margin-top:14px; font-size:13px; font-weight:600; color:var(--accent);}
  footer{text-align:center; padding:36px 0 10px; font-size:12px; color:var(--muted);}
  .empty{text-align:center; color:var(--muted); padding:60px 0; font-size:15px;}
</style>
</head>
<body>

<div class="hero">
  <span class="emoji">__SITE_EMOJI__</span>
  <h1>__SITE_TITLE__</h1>
  <div class="subtitle">__SITE_SUBTITLE__</div>
  <div class="count" id="count"></div>
</div>

<div class="grid" id="grid"></div>

<footer>由 build_index.py 自动生成 · 编辑 trips.json 后重新运行即可更新</footer>

<script type="application/json" id="trips-data">__TRIPS_JSON__</script>
<script>
  const data = JSON.parse(document.getElementById('trips-data').textContent);
  const grid = document.getElementById('grid');
  document.getElementById('count').textContent = '共 ' + data.trips.length + ' 段旅程';
  if (!data.trips.length) {
    grid.innerHTML = '<div class="empty">还没有行程，去添加第一段旅程吧 ✈️</div>';
  }
  data.trips.forEach(t => {
    const tags = (t.tags || []).map(x => '<span class="tag">'+x+'</span>').join('');
    const card = document.createElement('a');
    card.className = 'trip-card';
    card.href = t.file;
    card.innerHTML =
      '<div class="cover">'+(t.emoji||'🧳')+'</div>'+
      '<div class="body">'+
        '<h2>'+(t.title||t.file)+'</h2>'+
        '<div class="meta">📅 '+(t.dates||'')+'　·　🕓 更新 '+(t.updated||'')+'</div>'+
        '<div class="place">📍 '+(t.place||'')+'</div>'+
        '<div class="blurb">'+(t.blurb||'')+'</div>'+
        '<div class="tags">'+tags+'</div>'+
        '<div class="more">查看详情 →</div>'+
      '</div>';
    grid.appendChild(card);
  });
</script>
</body>
</html>
"""

html = (TEMPLATE
        .replace("__SITE_TITLE__", data["site"]["title"])
        .replace("__SITE_EMOJI__", data["site"]["emoji"])
        .replace("__SITE_SUBTITLE__", data["site"]["subtitle"])
        .replace("__TRIPS_JSON__", trips_json))

(ROOT / "index.html").write_text(html, encoding="utf-8")
print("OK: 已生成 index.html，共", len(data["trips"]), "段旅程")
