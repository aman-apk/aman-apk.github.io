# -*- coding: utf-8 -*-
"""مولّد موقع عائلة أمان — يقرأ أيقونات SVG الحية + الكاتالوغ ويصوغ index.html واحدة مكتفية بذاتها."""
import io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")

ICONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site_icons")
CATALOG = r"D:\Aman Labs\Ready\AmanStore\dist\catalog.json"
OUT = r"D:\Aman Labs\Ready\AmanWeb\index.html"

cat = json.load(io.open(CATALOG, encoding="utf-8"))
apps = sorted(cat["apps"], key=lambda a: a["index"])

def slug(pkg): return pkg.split(".")[-1]

# ═══ سبرايت الأيقونات: كل أيقونة تُعرَّف مرة واحدة وتُستنسخ بـ<use> ═══
sprite_parts = []
for a in apps:
    s = slug(a["packageName"])
    svg = io.open(os.path.join(ICONS, s + ".svg"), encoding="utf-8").read()
    inner = re.sub(r"^<svg[^>]*>", "", svg.strip())
    inner = re.sub(r"</svg>\s*$", "", inner)
    sprite_parts.append(f'<g id="i-{s}">{inner}</g>')
SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
          + "".join(sprite_parts) + "</defs></svg>")

def tile(s, extra_cls=""):
    return (f'<svg class="tile {extra_cls}" viewBox="0 0 108 108" aria-hidden="true">'
            f'<use href="#i-{s}"/></svg>')

def mb(n): return "%.1f MB" % (n / 1048576.0) if n < 1048576 * 99 else "%d MB" % round(n / 1048576.0)

store = next(a for a in apps if a["packageName"].endswith(".store"))
members = [a for a in apps if not a["packageName"].endswith(".store")]

# ═══ الكوكبة في البطل ═══
CONST = [
    ("mihrab",    "6%",  "12%", 74, 0.0), ("album",   "16%", "72%", 62, 1.1),
    ("kalamboard","30%", "6%",  56, 2.2), ("ruznama", "8%",  "44%", 66, 0.6),
    ("hisn",      "34%", "86%", 58, 1.7), ("jisr",    "46%", "16%", 62, 2.8),
    ("qamariya",  "52%", "74%", 68, 0.9), ("daftar",  "66%", "8%",  54, 1.4),
    ("sijil",     "70%", "84%", 56, 2.0), ("wathaiq", "80%", "20%", 64, 0.3),
    ("jezdan",    "86%", "66%", 52, 2.5), ("sitr",    "58%", "48%", 46, 1.9),
]
const_html = "".join(
    f'<div class="orb" style="top:{top};inset-inline-start:{start};width:{w}px;animation-delay:{d}s">{tile(s)}</div>'
    for s, top, start, w, d in CONST)

# ═══ بطاقات التطبيقات ═══
cards = []
for a in members:
    s = slug(a["packageName"])
    name_full = a["nameAr"]
    name, _, tag = name_full.partition(" — ")
    feats = "".join(f"<span>{f}</span>" for f in a["featuresAr"][:3])
    cards.append(f'''
      <article class="card reveal" style="--ac:{a['accentHex']}" data-pkg="{a['packageName']}">
        <div class="card-head">{tile(s)}
          <div><h3>{name}</h3><p class="tag">{tag}</p></div>
        </div>
        <p class="sum">{a['summaryAr']}</p>
        <div class="feats">{feats}</div>
        <div class="card-foot">
          <span class="meta"><b data-v>{a['versionName']}</b> · <span data-s>{mb(a['sizeBytes'])}</span></span>
          <a class="dl" data-dl href="{a['apkUrl']}" rel="nofollow">تنزيل APK</a>
        </div>
      </article>''')
CARDS = "".join(cards)

FALLBACK = json.dumps(
    {a["packageName"]: {"v": a["versionName"], "s": a["sizeBytes"], "u": a["apkUrl"]} for a in apps},
    ensure_ascii=False)

WIN_SETUP = "https://github.com/aman-apk/aman-releases/releases/download/v1.1.0/jisr-0.2.9-windows-x64-setup.exe"
WIN_ZIP   = "https://github.com/aman-apk/aman-releases/releases/download/v1.1.0/jisr-0.2.9-windows-x64-portable.zip"

HTML = f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>أمان لابز — عائلة تطبيقات الخصوصية العربية</title>
<meta name="description" content="أربعة عشر تطبيقًا عربيًا تعمل بلا إنترنت وبلا إعلانات وبلا تتبّع — بياناتك على جهازك وحده. نزّل متجر أمان وثبّت العائلة كلها.">
<meta property="og:title" content="أمان لابز — عائلة تطبيقات الخصوصية العربية">
<meta property="og:description" content="١٤ تطبيقًا عربيًا: بلا إعلانات، بلا تتبّع، بلا سحابة — وأكثرها يعمل دون اتصالٍ بالإنترنت.">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 108 108'%3E%3Crect width='108' height='108' rx='24' fill='%23131826'/%3E%3Ccircle cx='54' cy='54' r='20' fill='%23E0A32E'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Almarai:wght@400;700;800&display=swap" rel="stylesheet">
<style>
  :root {{
    --night:#0B0E15; --night2:#10141f; --panel:#131826; --panel2:#171d2e;
    --ink:#F2EDE3; --muted:#98A1B3; --gold:#E0A32E; --gold-deep:#B87708;
    --line:rgba(242,237,227,.09); --maxw:1180px;
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  html {{ scroll-behavior:smooth; }}
  body {{ font-family:'Almarai',system-ui,sans-serif; background:var(--night); color:var(--ink); overflow-x:hidden; line-height:1.7; }}
  ::selection {{ background:var(--gold); color:#221a05; }}
  a {{ color:inherit; text-decoration:none; }}
  .wrap {{ max-width:var(--maxw); margin:0 auto; padding:0 22px; }}

  /* ══ nav ══ */
  nav {{ position:fixed; inset-inline:0; top:0; z-index:50; backdrop-filter:blur(14px);
        background:rgba(11,14,21,.72); border-bottom:1px solid var(--line); }}
  .nav-in {{ max-width:var(--maxw); margin:0 auto; padding:10px 22px; display:flex; align-items:center; gap:26px; }}
  .brand {{ display:flex; align-items:center; gap:11px; font-weight:800; font-size:19px; }}
  .brand .tile {{ width:34px; height:34px; border-radius:9px; }}
  .navlinks {{ display:flex; gap:22px; font-size:14px; color:var(--muted); margin-inline-start:auto; }}
  .navlinks a:hover {{ color:var(--ink); }}
  .nav-cta {{ background:var(--gold); color:#221a05; font-weight:800; font-size:13.5px;
             padding:8px 18px; border-radius:999px; white-space:nowrap; }}
  .nav-cta:hover {{ background:#EDB84A; }}

  /* ══ hero ══ */
  header {{ position:relative; min-height:min(100svh, 940px); display:flex; align-items:center; overflow:hidden;
           background:
             radial-gradient(1100px 700px at 85% -8%, rgba(224,163,46,.16), transparent 62%),
             radial-gradient(900px 600px at 12% 110%, rgba(92,113,133,.20), transparent 60%),
             linear-gradient(160deg, #121826 0%, var(--night) 55%, #0A0C12 100%); }}
  .stars, .stars2 {{ position:absolute; inset:0; pointer-events:none; }}
  .stars {{ box-shadow:none; }}
  .star {{ position:absolute; width:2px; height:2px; border-radius:50%; background:#fff; opacity:.5;
          animation:tw 4.2s ease-in-out infinite; }}
  @keyframes tw {{ 0%,100% {{ opacity:.14; }} 50% {{ opacity:.62; }} }}
  .orb {{ position:absolute; opacity:.5; filter:saturate(.85);
         animation:float 9s ease-in-out infinite; will-change:transform; }}
  .orb .tile {{ width:100%; height:auto; border-radius:24%; box-shadow:0 10px 34px rgba(0,0,0,.45); }}
  @keyframes float {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-14px); }} }}
  .hero-in {{ position:relative; z-index:2; max-width:var(--maxw); margin:0 auto; padding:120px 22px 80px; }}
  .kicker {{ color:var(--gold); font-weight:800; letter-spacing:.5px; font-size:15px; margin-bottom:14px; }}
  h1 {{ font-size:clamp(34px, 6vw, 64px); font-weight:800; line-height:1.25; max-width:14em; }}
  .sub {{ color:var(--muted); font-size:clamp(15px,2vw,18.5px); max-width:34em; margin:22px 0 34px; }}
  .sub b {{ color:var(--ink); }}
  .ctas {{ display:flex; gap:14px; flex-wrap:wrap; align-items:center; }}
  .btn {{ display:inline-flex; align-items:center; gap:9px; font-weight:800; border-radius:14px;
         padding:15px 28px; font-size:16px; transition:transform .15s, box-shadow .15s; }}
  .btn:active {{ transform:scale(.97); }}
  .btn-gold {{ background:linear-gradient(135deg,#EDB84A,var(--gold)); color:#221a05;
              box-shadow:0 8px 28px rgba(224,163,46,.28); }}
  .btn-gold:hover {{ box-shadow:0 10px 36px rgba(224,163,46,.42); transform:translateY(-2px); }}
  .btn-ghost {{ border:1.5px solid var(--line); color:var(--ink); }}
  .btn-ghost:hover {{ border-color:rgba(224,163,46,.5); }}
  .chips {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:38px; }}
  .chip {{ border:1px solid var(--line); background:rgba(19,24,38,.6); color:var(--muted);
          border-radius:999px; padding:7px 16px; font-size:13px; }}
  .chip b {{ color:var(--gold); font-size:14.5px; }}

  /* ══ sections ══ */
  section {{ padding:88px 0; position:relative; }}
  .sec-k {{ color:var(--gold); font-weight:800; font-size:14px; margin-bottom:8px; }}
  h2 {{ font-size:clamp(26px,3.6vw,38px); font-weight:800; margin-bottom:12px; }}
  .lead {{ color:var(--muted); max-width:38em; font-size:16px; }}

  /* المبادئ */
  .prin {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:16px; margin-top:42px; }}
  .p-card {{ background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:24px; }}
  .p-card .ic {{ width:46px; height:46px; border-radius:13px; display:grid; place-items:center;
               background:rgba(224,163,46,.12); color:var(--gold); margin-bottom:14px; }}
  .p-card h3 {{ font-size:17px; margin-bottom:6px; }}
  .p-card p {{ color:var(--muted); font-size:13.5px; }}

  /* بطاقة المتجر */
  .store-card {{ margin-top:46px; background:linear-gradient(135deg, rgba(224,163,46,.14), rgba(19,24,38,.9) 45%);
               border:1px solid rgba(224,163,46,.35); border-radius:24px; padding:34px;
               display:flex; gap:28px; align-items:center; flex-wrap:wrap; }}
  .store-card .tile {{ width:104px; height:104px; border-radius:24px; flex-shrink:0;
                      box-shadow:0 12px 40px rgba(0,0,0,.5); }}
  .store-card h3 {{ font-size:24px; }} .store-card .en {{ color:var(--muted); font-size:13px; }}
  .store-card p.d {{ color:var(--muted); margin:8px 0 0; max-width:34em; }}
  .store-cta {{ margin-inline-start:auto; text-align:center; }}
  .store-cta .meta {{ display:block; color:var(--muted); font-size:12.5px; margin-top:9px; }}

  /* شبكة التطبيقات */
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:18px; margin-top:38px; }}
  .card {{ background:var(--panel); border:1px solid var(--line); border-radius:20px; padding:22px;
          display:flex; flex-direction:column; gap:14px; transition:transform .22s, border-color .22s, box-shadow .22s; }}
  .card:hover {{ transform:translateY(-6px); border-color:color-mix(in srgb, var(--ac) 55%, transparent);
               box-shadow:0 18px 44px -18px color-mix(in srgb, var(--ac) 55%, transparent); }}
  .card-head {{ display:flex; gap:14px; align-items:center; }}
  .card .tile {{ width:64px; height:64px; border-radius:15px; flex-shrink:0; box-shadow:0 6px 20px rgba(0,0,0,.35); }}
  .card h3 {{ font-size:19px; }}
  .card .tag {{ color:var(--muted); font-size:12.5px; }}
  .card .sum {{ font-size:14.5px; color:#C8CEDC; }}
  .feats {{ display:flex; flex-wrap:wrap; gap:7px; }}
  .feats span {{ font-size:11.5px; color:var(--muted); border:1px solid var(--line);
               border-radius:999px; padding:4px 11px; }}
  .card-foot {{ margin-top:auto; display:flex; align-items:center; justify-content:space-between; gap:10px; }}
  .meta {{ color:var(--muted); font-size:12.5px; }} .meta b {{ color:var(--ink); }}
  .dl {{ font-weight:800; font-size:13.5px; padding:9px 20px; border-radius:11px;
        background:color-mix(in srgb, var(--ac) 26%, var(--panel2)); color:var(--ink);
        border:1px solid color-mix(in srgb, var(--ac) 45%, transparent); transition:background .18s; }}
  .dl:hover {{ background:color-mix(in srgb, var(--ac) 42%, var(--panel2)); }}

  /* الحاسوب */
  .pc {{ margin-top:42px; background:linear-gradient(135deg,#232f3d,#141a24 60%);
        border:1px solid rgba(92,113,133,.4); border-radius:24px; padding:36px;
        display:flex; gap:30px; align-items:center; flex-wrap:wrap; }}
  .pc .tile {{ width:96px; height:96px; border-radius:22px; box-shadow:0 12px 40px rgba(0,0,0,.5); }}
  .pc h3 {{ font-size:22px; }} .pc p {{ color:var(--muted); max-width:30em; margin-top:6px; font-size:14.5px; }}
  .pc-btns {{ margin-inline-start:auto; display:flex; flex-direction:column; gap:10px; }}
  .pc-btns .btn {{ padding:12px 24px; font-size:14.5px; justify-content:center; }}
  .pc-note {{ color:var(--muted); font-size:12px; text-align:center; }}

  /* كيف يصلك */
  .steps {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:16px; margin-top:42px; counter-reset:st; }}
  .step {{ background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:26px; position:relative; }}
  .step::before {{ counter-increment:st; content:counter(st); position:absolute; top:-16px; inset-inline-start:22px;
                 width:34px; height:34px; border-radius:50%; background:var(--gold); color:#221a05;
                 font-weight:800; display:grid; place-items:center; font-size:16px; }}
  .step h3 {{ margin:8px 0 6px; font-size:17px; }} .step p {{ color:var(--muted); font-size:13.5px; }}

  /* الثقة */
  .trust {{ background:linear-gradient(180deg, var(--night2), var(--night)); border-block:1px solid var(--line); }}
  .trust-in {{ display:grid; grid-template-columns:1.1fr 1fr; gap:44px; align-items:center; }}
  .t-list {{ display:flex; flex-direction:column; gap:16px; margin-top:26px; }}
  .t-item {{ display:flex; gap:13px; align-items:flex-start; }}
  .t-item .ic {{ flex-shrink:0; width:38px; height:38px; border-radius:11px; display:grid; place-items:center;
               background:rgba(224,163,46,.12); color:var(--gold); }}
  .t-item b {{ display:block; font-size:15.5px; }}
  .t-item p {{ color:var(--muted); font-size:13px; }}
  .t-links {{ margin-top:26px; display:flex; gap:16px; flex-wrap:wrap; font-size:13.5px; }}
  .t-links a {{ color:var(--gold); border-bottom:1px dashed rgba(224,163,46,.4); padding-bottom:2px; }}
  .t-visual {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; direction:ltr; }}
  .t-visual .tile {{ width:100%; height:auto; border-radius:20%; opacity:.92;
                    box-shadow:0 8px 26px rgba(0,0,0,.4); transition:transform .2s; }}
  .t-visual .tile:hover {{ transform:scale(1.06); }}

  footer {{ padding:52px 0 40px; border-top:1px solid var(--line); }}
  .f-in {{ display:flex; gap:26px; align-items:center; flex-wrap:wrap; }}
  .f-note {{ color:var(--muted); font-size:12.5px; margin-inline-start:auto; text-align:end; }}
  .f-links {{ display:flex; gap:18px; font-size:13.5px; color:var(--muted); }}
  .f-links a:hover {{ color:var(--gold); }}

  .reveal {{ opacity:0; transform:translateY(22px); transition:opacity .6s ease, transform .6s ease; }}
  .reveal.in {{ opacity:1; transform:none; }}

  @media (max-width: 900px) {{
    .navlinks {{ display:none; }}
    .trust-in {{ grid-template-columns:1fr; }}
    .orb {{ display:none; }}
    .orb:nth-child(-n+5) {{ display:block; opacity:.3; }}
    .store-cta, .pc-btns {{ margin-inline-start:0; width:100%; }}
    .pc-btns {{ flex-direction:row; flex-wrap:wrap; }}
    header {{ min-height:auto; }}
    .hero-in {{ padding:110px 22px 64px; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .star, .orb {{ animation:none; }}
    .reveal {{ opacity:1; transform:none; transition:none; }}
  }}
</style>
</head>
<body>
{SPRITE}

<nav>
  <div class="nav-in">
    <a class="brand" href="#top">{tile("store")} أمان لابز</a>
    <div class="navlinks">
      <a href="#apps">التطبيقات</a><a href="#principles">مبادئنا</a>
      <a href="#pc">للحاسوب</a><a href="#trust">الثقة</a>
    </div>
    <a class="nav-cta" data-store-dl href="{store['apkUrl']}">نزّل المتجر</a>
  </div>
</nav>

<header id="top">
  <div class="stars" aria-hidden="true"></div>
  {const_html}
  <div class="hero-in">
    <p class="kicker">عائلة أمان · Aman Labs</p>
    <h1>تطبيقاتٌ عربيةٌ تعمل لك،<br>لا عليك.</h1>
    <p class="sub">أربعة عشر تطبيقًا وُلدت في بيتٍ واحد: <b>بلا إعلانات، بلا تتبّع، بلا سحابة</b>. بياناتك تبقى على جهازك، وأكثر التطبيقات يعمل دون اتصالٍ بالإنترنت أصلًا.</p>
    <div class="ctas">
      <a class="btn btn-gold" data-store-dl href="{store['apkUrl']}">⬇ نزّل متجر أمان (APK)</a>
      <a class="btn btn-ghost" href="#apps">استعرض العائلة</a>
    </div>
    <div class="chips">
      <span class="chip"><b>14</b> تطبيقًا</span>
      <span class="chip"><b>0</b> إعلانات</span>
      <span class="chip"><b>0</b> متتبّعات</span>
      <span class="chip"><b>100%</b> عربي أولًا</span>
    </div>
  </div>
</header>

<section id="principles">
  <div class="wrap">
    <p class="sec-k">مبادئنا</p>
    <h2>الخصوصية عندنا مبدأ، لا إعداد</h2>
    <p class="lead">لا نطلب منك أن تثق بوعودنا — نبني التطبيق بحيث لا يحتاج ثقتك أصلًا.</p>
    <div class="prin">
      <div class="p-card reveal"><div class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 1l22 22M9 9a7 7 0 0 1 10 6M5 12a11 11 0 0 1 2.6-3.4M12 20h.01M8.5 16.5a5 5 0 0 1 5.5-1"/></svg></div>
        <h3>بلا إنترنت حيث يجب</h3><p>الوثائق والتقويم والإشعارات والسِتر: حزمها لا تحمل إذن الإنترنت أصلًا — تحقّق بنفسك من إعدادات النظام.</p></div>
      <div class="p-card reveal"><div class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-3 8-10V5l-8-3-8 3v7c0 7 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg></div>
        <h3>توقيع يُفحص قبل التثبيت</h3><p>متجر أمان يطابق بصمة توقيع كل حزمة مع بصمتها المثبّتة لديه — حزمة مزوّرة لا تمرّ.</p></div>
      <div class="p-card reveal"><div class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="9" height="14" rx="2"/><rect x="13" y="4" width="9" height="14" rx="2"/><path d="M6.5 17h.01M17.5 15h.01"/></svg></div>
        <h3>ينتشر جهازًا لجهاز</h3><p>المتجر وتطبيقاته تُشارَك بالقرب دون إنترنت — يكفي أن يملكه صديقك ليصلك كل شيء.</p></div>
      <div class="p-card reveal"><div class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg></div>
        <h3>عربيٌّ أولًا</h3><p>من اليمين إلى اليسار تصميمًا لا ترجمةً — بخط المراعي وذوقٍ واحد يجمع العائلة كلها.</p></div>
    </div>
  </div>
</section>

<section id="apps" style="padding-top:20px">
  <div class="wrap">
    <p class="sec-k">العائلة</p>
    <h2>أربعة عشر فردًا، بيتٌ واحد</h2>
    <p class="lead">كل تطبيقٍ يسدّ حاجةً يومية حقيقية — ويشارك إخوته المبدأ نفسه: بياناتك ملكك وحدك.</p>

    <div class="store-card reveal" data-pkg="{store['packageName']}">
      {tile("store")}
      <div>
        <h3>متجر أمان <span class="en">· Aman Store</span></h3>
        <p class="d">{store['descriptionAr']}</p>
      </div>
      <div class="store-cta">
        <a class="btn btn-gold" data-store-dl href="{store['apkUrl']}">⬇ تنزيل المتجر</a>
        <span class="meta">الإصدار <b data-v>{store['versionName']}</b> · <span data-s>{mb(store['sizeBytes'])}</span> · أندرويد 7+</span>
      </div>
    </div>

    <div class="grid">{CARDS}</div>
  </div>
</section>

<section id="pc" style="padding-top:10px">
  <div class="wrap">
    <p class="sec-k">للحاسوب</p>
    <h2>جسرٌ يصل هاتفك بحاسوبك</h2>
    <div class="pc reveal">
      {tile("jisr")}
      <div>
        <h3>جسر لويندوز</h3>
        <p>انقل الملفات بين هاتفك وحاسوبك عبر شبكتك المحلية وحدها — بلا كابل ولا سحابة ولا حدود حجم.</p>
      </div>
      <div class="pc-btns">
        <a class="btn btn-gold" href="{WIN_SETUP}">⬇ المثبّت (Setup)</a>
        <a class="btn btn-ghost" href="{WIN_ZIP}">نسخة محمولة (ZIP)</a>
        <span class="pc-note">ويندوز 10/11 · 64bit</span>
      </div>
    </div>
  </div>
</section>

<section id="how" style="padding-top:10px">
  <div class="wrap">
    <p class="sec-k">كيف يصلك أمان؟</p>
    <h2>ثلاث خطوات، ثم لا حاجة للإنترنت</h2>
    <div class="steps">
      <div class="step reveal"><h3>نزّل متجر أمان</h3><p>ملف APK واحد من هذه الصفحة — ثبّته واسمح بمصادر التثبيت حين يسألك أندرويد.</p></div>
      <div class="step reveal"><h3>ثبّت ما تحب</h3><p>تصفح العائلة داخل المتجر وثبّت بنقرة — المتجر يفحص توقيع كل حزمة قبل تثبيتها.</p></div>
      <div class="step reveal"><h3>شاركه من جهازٍ لجهاز</h3><p>مرّر المتجر وتطبيقاته لأهلك وأصدقائك بالمشاركة القريبة أو عبر جسر — بلا إنترنت إطلاقًا.</p></div>
    </div>
  </div>
</section>

<section id="trust" class="trust">
  <div class="wrap trust-in">
    <div>
      <p class="sec-k">الثقة تُبنى بالهندسة</p>
      <h2>شفافيةٌ يمكنك التحقق منها بنفسك</h2>
      <div class="t-list">
        <div class="t-item reveal"><div class="ic">🔏</div><div><b>بصمات توقيع معلنة ومثبّتة</b><p>بصمة SHA-256 لتوقيع كل تطبيق منشورة في كاتالوغ عام، والمتجر يرفض أي حزمة تخالفها.</p></div></div>
        <div class="t-item reveal"><div class="ic">🧾</div><div><b>بصمة لكل ملف</b><p>لكل حزمة sha256 معلنة — تستطيع التحقق من أي ملف نزّلته بنفسك قبل تثبيته.</p></div></div>
        <div class="t-item reveal"><div class="ic">🛡</div><div><b>حارس بناءٍ صارم</b><p>التطبيقات الحساسة تُبنى بحارسٍ يفشل البناء كله إن تسلّلت أي مكتبة شبكية أو إذنٌ غير مبرَّر.</p></div></div>
        <div class="t-item reveal"><div class="ic">🗝</div><div><b>بياناتك تغادر معك فقط</b><p>نسخ احتياطي موحّد مشفّر بمفتاحٍ تحفظه أنت — لا حسابات ولا خوادم ولا «مزامنة» خفية.</p></div></div>
      </div>
      <div class="t-links">
        <a href="https://github.com/aman-apk/aman-releases/blob/main/catalog.json" rel="noopener">كاتالوغ الشفافية</a>
        <a href="https://github.com/aman-apk/aman-releases/releases/tag/v1.1.0" rel="noopener">كل الإصدارات على GitHub</a>
      </div>
    </div>
    <div class="t-visual" aria-hidden="true">
      {tile("mihrab")}{tile("kalamboard")}{tile("album")}{tile("ruznama")}
      {tile("hisn")}{tile("wathaiq")}{tile("jisr")}{tile("daftar")}
      {tile("sijil")}{tile("jezdan")}{tile("diwan")}{tile("sitr")}
    </div>
  </div>
</section>

<footer>
  <div class="wrap f-in">
    <a class="brand" href="#top">{tile("store")} أمان لابز</a>
    <div class="f-links">
      <a href="https://wa.me/963980690860" rel="noopener">تواصل واتساب</a>
      <a href="https://github.com/aman-apk" rel="noopener">GitHub</a>
    </div>
    <p class="f-note">هذا عنوانٌ مؤقت ريثما يستقر الدومين الدائم.<br>صُنع بحبٍّ في بيت أمان · {cat['publisher']['nameAr']} © 2026</p>
  </div>
</footer>

<script>
  // نجوم البطل
  (function () {{
    var host = document.querySelector('.stars');
    for (var i = 0; i < 70; i++) {{
      var s = document.createElement('span');
      s.className = 'star';
      s.style.top = (Math.random() * 100) + '%';
      s.style.insetInlineStart = (Math.random() * 100) + '%';
      s.style.animationDelay = (Math.random() * 4).toFixed(2) + 's';
      s.style.animationDuration = (3 + Math.random() * 4).toFixed(2) + 's';
      var d = Math.random();
      s.style.width = s.style.height = (d < .8 ? 2 : 3) + 'px';
      host.appendChild(s);
    }}
  }})();

  // كشف تدريجي
  (function () {{
    var io = new IntersectionObserver(function (es) {{
      es.forEach(function (e) {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }});
    }}, {{ threshold: .12 }});
    document.querySelectorAll('.reveal').forEach(function (el) {{ io.observe(el); }});
  }})();

  // الكاتالوغ الحي: النسخ والأحجام والروابط تُحدَّث من المصدر نفسه الذي يقرؤه المتجر
  (function () {{
    var FB = {FALLBACK};
    function mb(n) {{ return (n / 1048576).toFixed(1) + ' MB'; }}
    function apply(map) {{
      document.querySelectorAll('[data-pkg]').forEach(function (card) {{
        var a = map[card.getAttribute('data-pkg')]; if (!a) return;
        var v = card.querySelector('[data-v]'); if (v) v.textContent = a.v;
        var s = card.querySelector('[data-s]'); if (s) s.textContent = mb(a.s);
        var d = card.querySelector('[data-dl]'); if (d) d.href = a.u;
      }});
      var st = map['org.amanlabs.store'];
      if (st) document.querySelectorAll('[data-store-dl]').forEach(function (b) {{ b.href = st.u; }});
    }}
    apply(FB);
    fetch('https://raw.githubusercontent.com/aman-apk/aman-releases/main/catalog.json', {{ cache: 'no-store' }})
      .then(function (r) {{ return r.json(); }})
      .then(function (c) {{
        var m = {{}};
        c.apps.forEach(function (a) {{ m[a.packageName] = {{ v: a.versionName, s: a.sizeBytes, u: a.apkUrl }}; }});
        apply(m);
      }})
      .catch(function () {{}});
  }})();
</script>
</body>
</html>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8").write(HTML)
print("site written:", OUT, len(HTML), "chars")
