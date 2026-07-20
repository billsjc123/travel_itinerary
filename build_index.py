#!/usr/bin/env python3
# 读取 trips.json，生成自包含的 index.html（数据内联，本地/Pages 均可）。
# 主页按「年」分组展示所有行程，hero 带全幅背景图。
# 用法：python3 build_index.py
import json, pathlib, base64

ROOT = pathlib.Path(__file__).resolve().parent
data = json.loads((ROOT / "trips.json").read_text(encoding="utf-8"))
trips_json = json.dumps(data, ensure_ascii=False)

# Hero 背景图（与 build_index.py 同目录下的 hero-bg.jpg）
hero_bg_path = ROOT / "hero-bg.jpg"
if not hero_bg_path.exists():
    # 也支持 .png / .jpeg 等常见扩展名
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = ROOT / ("hero-bg" + ext)
        if p.exists():
            hero_bg_path = p
            break
if not hero_bg_path.exists():
    raise FileNotFoundError("未找到 hero-bg.jpg（请将背景图放到本目录并命名为 hero-bg.jpg）")

mime = {".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png",".webp":"image/webp"}
ext = hero_bg_path.suffix.lower()
b64 = base64.b64encode(hero_bg_path.read_bytes()).decode("ascii")
data_uri = f"data:{mime.get(ext,'image/jpeg')};base64,{b64}"

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
  /* Hero with full-bleed background image */
  .hero{
    position:relative; text-align:center; padding:80px 20px 50px;
    color:#fff; overflow:hidden; border-radius:var(--radius);
    background:url('__HERO_BG__') center center/cover no-repeat;
  }
  .hero::before{
    content:''; position:absolute; inset:0;
    background:linear-gradient(180deg,rgba(0,0,0,.45),rgba(0,0,0,.65));
    z-index:0;
  }
  .hero > *{ position:relative; z-index:1; }
  .hero h1{ font-size:34px; letter-spacing:.5px; text-shadow:0 2px 12px rgba(0,0,0,.4); }
  .hero .subtitle{ font-size:16px; color:rgba(255,255,255,.88); margin-top:10px; text-shadow:0 1px 8px rgba(0,0,0,.35); }
  .count{ display:inline-block; margin-top:18px; font-size:13px; color:rgba(255,255,255,.85);
    background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.25);
    border-radius:999px; padding:6px 18px; backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px); }

  /* Year group */
  .year{ font-size:22px; font-weight:700; margin:36px 0 4px; padding-left:8px;
    border-left:4px solid var(--accent); }

  /* Grid */
  .grid{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:20px; margin-top:18px;}
  .trip-card{ background:var(--card); border:1px solid var(--border); border-radius:var(--radius);
    box-shadow:var(--shadow); overflow:hidden; display:flex; flex-direction:column;
    transition:transform .15s ease, box-shadow .15s ease;}
  .trip-card:hover{ transform:translateY(-4px); box-shadow:0 8px 24px rgba(0,0,0,.13);}
  .cover{ height:120px; display:flex; align-items:center; justify-content:center;
    background:linear-gradient(135deg,#c0392b,#e67e22); font-size:54px;}
  .body{ padding:16px 18px 20px; display:flex; flex-direction:column; flex:1;}
  .body h2{ font-size:18px; font-weight:700;}
  .meta{ font-size:12.5px; color:var(--muted); margin-top:4px;}
  .place{ font-size:12.5px; color:var(--muted); margin-top:2px;}
  .blurb{ font-size:13px; color:#444; margin-top:10px; flex:1;}
  .tags{ margin-top:12px; display:flex; gap:6px; flex-wrap:wrap;}
  .tag{ font-size:11px; padding:2px 10px; border-radius:99px; background:#f0f0f0; color:#555;}
  .more{ margin-top:14px; font-size:13px; font-weight:600; color:var(--accent);}
  .empty{ text-align:center; color:var(--muted); padding:60px 0; font-size:15px;}
</style>
</head>
<body>

<div class="hero">
  <h1>__SITE_TITLE__</h1>
  <div class="subtitle">__SITE_SUBTITLE__</div>
  <div class="count" id="count"></div>
</div>

<div id="content"></div>

<script type="application/json" id="trips-data">__TRIPS_JSON__</script>
<script>
  const data = JSON.parse(document.getElementById('trips-data').textContent);
  const content = document.getElementById('content');
  document.getElementById('count').textContent = '共 ' + data.trips.length + ' 段旅程';

  function makeCard(t){
    const tags = (t.tags || []).map(x => '<span class="tag">'+x+'</span>').join('');
    const card = document.createElement('a');
    card.className = 'trip-card';
    card.href = t.file;
    card.innerHTML =
      '<div class="cover">'+(t.emoji||'🧳')+'</div>'+
      '<div class="body">'+
        '<h2>'+(t.title||t.file)+'</h2>'+
        '<div class="meta">📅 '+(t.dates||'')+'　·　🕒 更新 '+(t.updated||'')+'</div>'+
        '<div class="place">📍 '+(t.place||'')+'</div>'+
        '<div class="blurb">'+(t.blurb||'')+'</div>'+
        '<div class="tags">'+tags+'</div>'+
        '<div class="more">查看详情 →</div>'+
      '</div>';
    return card;
  }

  if (!data.trips.length) {
    content.innerHTML = '<div class="empty">还没有行程，去添加第一段旅程吧 ✈️</div>';
  } else {
    const years = {};
    data.trips.forEach(t => {
      const y = t.year || (t.dates && (t.dates.match(/\d{4}/) || [])[0]) || '未知';
      (years[y] = years[y] || []).push(t);
    });
    Object.keys(years).sort().reverse().forEach(y => {
      const h = document.createElement('div');
      h.className = 'year';
      h.textContent = y + ' 年';
      content.appendChild(h);
      const grid = document.createElement('div');
      grid.className = 'grid';
      years[y].forEach(t => grid.appendChild(makeCard(t)));
      content.appendChild(grid);
    });
  }
</script>
</body>
</html>
"""

html = (TEMPLATE
        .replace("__SITE_TITLE__", data["site"]["title"])
        .replace("__SITE_SUBTITLE__", data["site"]["subtitle"])
        .replace("__HERO_BG__", data_uri)
        .replace("__TRIPS_JSON__", trips_json))

(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"OK: 已生成 index.html（含 hero 背景图 {len(b64)} 字符），共 {len(data['trips'])} 段旅程")
