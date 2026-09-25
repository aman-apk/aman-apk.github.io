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

store = next(a for a in apps if a["packageName"].endswith(".store"))
members = [a for a in apps if not a["packageName"].endswith(".store")]
# التغبيش (حركة المالك التسويقية 2026-09-18): المغبَّش في الكاتالوغ لا يظهر في الموقع إلا بطاقةً
# ضبابية بلا اسمٍ ولا أيقونةٍ ولا رابط — ولا تدخل أيقونتُه السبرايت ولا الكوكبة ولا لوحة الثقة،
# فلا تُستشفّ هويته من مصدر الصفحة. الحالة الحية تُقلب من المتصفح (انظر applyHidden أسفل الصفحة).
shown = [a for a in members if not a.get("hidden")]
hidden_members = [a for a in members if a.get("hidden")]
shown_slugs = {slug(a["packageName"]) for a in shown}

# ═══ سبرايت الأيقونات: كل أيقونة تُعرَّف مرة واحدة وتُستنسخ بـ<use> ═══
sprite_parts = []
for a in [store] + shown:
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

# ═══ الكوكبة في البطل ═══
CONST = [
    ("mihrab",    "6%",  "12%", 74, 0.0), ("album",   "16%", "72%", 62, 1.1),
    ("kalamboard","30%", "6%",  56, 2.2), ("ruznama", "8%",  "44%", 66, 0.6),
    ("hisn",      "34%", "86%", 58, 1.7), ("jisr",    "46%", "16%", 62, 2.8),
    ("qamariya",  "52%", "74%", 68, 0.9), ("daftar",  "66%", "8%",  54, 1.4),
    ("sijil",     "70%", "84%", 56, 2.0), ("wathaiq", "80%", "20%", 64, 0.3),
    ("jezdan",    "86%", "66%", 52, 2.5), ("sitr",    "58%", "48%", 46, 1.9),
]
orbit_tiles = "".join(tile(slug(a["packageName"])) for a in shown)  # بلا بلاطة المتجر بأمر المالك — ولا مغبَّش

const_html = "".join(
    f'<div class="orb" style="top:{top};inset-inline-start:{start};width:{w}px;animation-delay:{d}s">{tile(s)}</div>'
    for s, top, start, w, d in CONST if s in shown_slugs)

# بطاقة العضو المغبَّش: هويةٌ عامة وضبابٌ — معرِّفها رقمُ الترتيب وحده (لا حزمة ولا اسم في المصدر)
def teaser_card(idx):
    return (f'<article class="card teaser reveal" data-tz="{idx}">'
            f'<div class="card-head"><span class="tile tz"><i></i><b>✦</b></span>'
            f'<div><h3 class="blur">عضوٌ جديد في العائلة</h3><p class="tag">يُكشف عند إطلاقه</p></div></div>'
            f'<p class="sum blur">تطبيقٌ آخر يولد في بيت أمان — بلا إعلانات ولا تتبّع ولا سحابة</p>'
            f'<div class="feats"><span>قريباً</span><span>تابع القناة</span></div>'
            f'<div class="card-foot"><span class="meta">قريباً</span><span class="dl soon">قريباً</span></div>'
            f'</article>')

# ═══ بطاقات التطبيقات (عربية وإنكليزية من الحقول نفسها) ═══
def build_cards(lang):
    ar = lang == "ar"
    out = []
    for a in members:
        if a.get("hidden"):
            out.append(teaser_card(a["index"]) if ar else teaser_card_en(a["index"]))
            continue
        s_ = slug(a["packageName"])
        name_full = a["nameAr"] if ar else a["nameEn"]
        name, _, tag = name_full.partition(" — ")
        feats = "".join(f"<span>{f}</span>" for f in (a["featuresAr"] if ar else a["featuresEn"])[:3])
        out.append(f'''
      <article class="card reveal" style="--ac:{a['accentHex']}" data-pkg="{a['packageName']}">
        <div class="card-head">{tile(s_)}
          <div><h3>{name}</h3><p class="tag">{tag}</p></div>
        </div>
        <p class="sum">{a['summaryAr'] if ar else a['summaryEn']}</p>
        <div class="feats">{feats}</div>
        <div class="card-foot">
          <span class="meta"><b data-v>{a['versionName']}</b> · <span data-s>{mb(a['sizeBytes'])}</span></span>
          <a class="dl" data-dl href="{a['apkUrl']}" rel="nofollow">{"تنزيل APK" if ar else "Download APK"}</a>
        </div>
      </article>''')
    return "".join(out)
def teaser_card_en(idx):
    return (f'<article class="card teaser reveal" data-tz="{idx}">'
            f'<div class="card-head"><span class="tile tz"><i></i><b>✦</b></span>'
            f'<div><h3 class="blur">A new family member</h3><p class="tag">Revealed at launch</p></div></div>'
            f'<p class="sum blur">Another app born in the Aman house — no ads, no tracking, no cloud</p>'
            f'<div class="feats"><span>Soon</span><span>Stay tuned</span></div>'
            f'<div class="card-foot"><span class="meta">Soon</span><span class="dl soon">Soon</span></div>'
            f'</article>')
CARDS = build_cards("ar")
CARDS_EN = build_cards("en")
# الاحتياط المضمَّن: الأعضاء الظاهرون والمتجر فقط — لا رابطَ ولا حزمةَ مغبَّشٍ في مصدر الصفحة
FALLBACK = json.dumps(
    {a["packageName"]: {"v": a["versionName"], "s": a["sizeBytes"], "u": a["apkUrl"]} for a in [store] + shown},
    ensure_ascii=False)

# عبر مرآة كلاودفلير — الووركر يخدم exe/zip أيضاً منذ 2026-09-03
WIN_SETUP = "https://dl.amanlabs.app/jisr-0.2.9-windows-x64-setup.exe"
WIN_ZIP   = "https://dl.amanlabs.app/jisr-0.2.9-windows-x64-portable.zip"
# طيف لسطح المكتب (2026-09-08): كروميوم حقيقي عبر CEF، لا صفحة ويب في إطار.
# مثبّت exe لا msi: مرآة كلاودفلير تخدم apk/exe/zip فقط (worker.js)
TAYF_WIN_SETUP = "https://dl.amanlabs.app/tayf-desktop-0.1.12-windows-x64-setup.exe"
TAYF_WIN_ZIP   = "https://dl.amanlabs.app/tayf-desktop-0.1.12-windows-x64-portable.zip"

from urllib.parse import quote
WA_REQUEST = "https://wa.me/963943558806?text=" + quote("طلب مشروع خاص: ")
WA_REPORT  = "https://wa.me/963943558806?text=" + quote("بلاغ مشكلة: ")

HTML = f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مختبرات أمان — عائلة تطبيقات الخصوصية العربية</title>
<meta name="description" content="أربعة عشر تطبيقاً عربياً تعمل بلا إنترنت وبلا إعلانات وبلا تتبّع — بياناتك على جهازك وحده. نزّل متجر أمان وثبّت العائلة كلها.">
<meta property="og:title" content="مختبرات أمان — عائلة تطبيقات الخصوصية العربية">
<meta property="og:description" content="١٤ تطبيقاً عربياً: بلا إعلانات، بلا تتبّع، بلا سحابة — وأكثرها يعمل دون اتصالٍ بالإنترنت.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://amanlabs.app/">
<link rel="canonical" href="https://amanlabs.app/">
<link rel="alternate" hreflang="en" href="https://amanlabs.app/en/">
<link rel="alternate" hreflang="ar" href="https://amanlabs.app/">
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
  /* header عنصر flex فحاوي البطل عنصرٌ مرن يتمدّد إلى عرض محتواه (شريط الأيقونات max-content = 850px)
     فينزاح كلُّ الصفحة على الهاتف — min-width:0 + width:100% يثبّتانه على عرض الشاشة (بلاغ المالك 2026-09-25) */
  .hero-in {{ position:relative; z-index:2; max-width:var(--maxw); width:100%; min-width:0; margin:0 auto; padding:120px 22px 80px; }}
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
  /* العضو المغبَّش: بلاطة زجاجٍ مصنفر بشرارة، نصٌّ مضبَّب، وزرٌّ متقطّع بلا رابط */
  .card.teaser {{ --ac:#E0A32E; }}
  .card.teaser:hover {{ transform:none; }}
  .tile.tz {{ position:relative; display:grid; place-items:center; width:64px; height:64px; border-radius:15px; flex-shrink:0;
              background:linear-gradient(160deg, rgba(224,163,46,.45), rgba(124,137,207,.40) 55%, rgba(217,124,147,.35));
              box-shadow:0 6px 20px rgba(0,0,0,.35); overflow:hidden; }}
  .tile.tz i {{ position:absolute; inset:0; background:rgba(255,255,255,.07); backdrop-filter:blur(6px); -webkit-backdrop-filter:blur(6px); }}
  .tile.tz b {{ position:relative; color:#FFF7E2; font-size:30px; line-height:1; text-shadow:0 2px 6px rgba(0,0,0,.35); }}
  .card.teaser .blur {{ filter:blur(5px); opacity:.6; user-select:none; }}
  .dl.soon {{ border-style:dashed; opacity:.7; cursor:default; }}

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
  .twrap {{ position:relative; display:inline-flex; flex-shrink:0; }}
  .tcount {{ position:absolute; inset-inline-start:-6px; bottom:-7px; display:inline-flex; align-items:center; gap:3px; padding:3px 8px 3px 6px; border-radius:999px;
             background:linear-gradient(135deg, rgba(14,17,26,.97), rgba(34,30,22,.97)); color:#F5D27A; font-size:11.5px; font-weight:800; line-height:1;
             border:1px solid rgba(240,205,122,.55); box-shadow:0 4px 12px rgba(0,0,0,.45), 0 0 0 3px var(--panel), 0 0 14px rgba(224,163,46,.25);
             animation:trise .5s cubic-bezier(.2,.8,.2,1) both; }}
  .tcount svg {{ width:11px; height:11px; color:var(--gold); }}
  .tcount small {{ font-size:9.5px; font-weight:600; color:rgba(245,210,122,.75); margin-inline-start:1px; }}
  .store-card .tcount {{ font-size:13px; padding:4px 10px 4px 8px; bottom:-9px; }}
  @keyframes trise {{ from {{ opacity:0; transform:translateY(5px) scale(.85); }} to {{ opacity:1; transform:none; }} }}
  .t-list {{ display:flex; flex-direction:column; gap:16px; margin-top:26px; }}
  .t-item {{ display:flex; gap:13px; align-items:flex-start; }}
  .t-item .ic {{ flex-shrink:0; width:38px; height:38px; border-radius:11px; display:grid; place-items:center;
               background:rgba(224,163,46,.12); color:var(--gold); }}
  .t-item b {{ display:block; font-size:15.5px; }}
  .t-item p {{ color:var(--muted); font-size:13px; }}
  .t-visual {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; direction:ltr; }}
  .t-visual .tile {{ width:100%; height:auto; border-radius:20%; opacity:.92;
                    box-shadow:0 8px 26px rgba(0,0,0,.4); transition:transform .2s; }}
  .t-visual .tile:hover {{ transform:scale(1.06); }}

  /* خدماتنا — بروح بنر المتجر: توهّج عنبري و«فكرة» ذهبية وزر محدَّد */
  .svc {{ margin-top:38px; position:relative; border-radius:24px; padding:36px;
         background:
           radial-gradient(560px 320px at 88% 0%, rgba(224,163,46,.20), transparent 60%),
           linear-gradient(135deg, var(--panel2), var(--panel) 70%);
         border:1px solid rgba(224,163,46,.35); overflow:hidden; }}
  .svc-body {{ color:#D8DCE8; font-size:16.5px; max-width:44em; line-height:1.95; }}
  .svc-feats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:12px; margin-top:24px; }}
  .svc-f {{ display:flex; align-items:center; gap:10px; background:rgba(11,14,21,.5);
           border:1px solid var(--line); border-radius:14px; padding:13px 16px; font-size:13.5px; }}
  .svc-f span {{ font-size:18px; }}
  .svc-cta {{ border-color:rgba(224,163,46,.6); color:var(--gold); }}
  .svc-cta:hover {{ background:rgba(224,163,46,.1); border-color:var(--gold); }}
  .svc-strip {{ margin-top:16px; background:var(--panel); border:1px solid var(--line); border-radius:18px;
               padding:20px 24px; display:flex; gap:18px; align-items:center; flex-wrap:wrap; }}
  .svc-strip p {{ color:var(--muted); font-size:13.5px; max-width:46em; }}
  .svc-strip b {{ color:var(--ink); }}
  .svc-strip a {{ margin-inline-start:auto; color:var(--gold); font-size:13.5px; font-weight:800;
                 border-bottom:1px dashed rgba(224,163,46,.4); padding-bottom:2px; white-space:nowrap; }}

  footer {{ padding:52px 0 40px; border-top:1px solid var(--line); }}
  .f-in {{ display:flex; gap:26px; align-items:center; flex-wrap:wrap; }}
  .f-note {{ color:var(--muted); font-size:12.5px; margin-inline-start:auto; text-align:end; }}
  .f-links {{ display:flex; gap:18px; font-size:13.5px; color:var(--muted); }}
  .f-links a:hover {{ color:var(--gold); }}

  .reveal {{ opacity:0; transform:translateY(22px); transition:opacity .6s ease, transform .6s ease; }}
  .reveal.in {{ opacity:1; transform:none; }}

  /* حزام العائلة — بديل الكوكبة على الشاشات الضيقة: صفٌّ ينساب بحواف ذائبة */
  .orbit {{ display:none; margin-top:38px; overflow:hidden; direction:ltr; max-width:100%;
    -webkit-mask-image:linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent);
    mask-image:linear-gradient(90deg, transparent, #000 12%, #000 88%, transparent); }}
  .orbit-track {{ display:flex; gap:14px; width:max-content; direction:ltr;
    animation:orbitflow 40s linear infinite; padding:8px 0 14px; }}
  .orbit .tile {{ width:58px; height:58px; border-radius:14px; flex-shrink:0;
    box-shadow:0 8px 20px rgba(0,0,0,.45); }}
  .orbit-track .tile:nth-child(odd) {{ transform:translateY(8px); }}
  @keyframes orbitflow {{ from {{ transform:translateX(0); }} to {{ transform:translateX(-50%); }} }}

  @media (max-width: 900px) {{
    .navlinks {{ display:none; }}
    .trust-in {{ grid-template-columns:1fr; }}
    .orb {{ display:none; }}
    .orbit {{ display:block; }}
    .store-cta, .pc-btns {{ margin-inline-start:0; width:100%; }}
    .pc-btns {{ flex-direction:row; flex-wrap:wrap; }}
    header {{ min-height:auto; }}
    .hero-in {{ padding:110px 22px 64px; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .star, .orb {{ animation:none; }}
    .orbit-track {{ animation:none; }}
    .reveal {{ opacity:1; transform:none; transition:none; }}
  }}
</style>
</head>
<body>
{SPRITE}

<nav>
  <div class="nav-in">
    <a class="brand" href="#top">{tile("store")} مختبرات أمان</a>
    <div class="navlinks">
      <a href="#apps">التطبيقات</a><a href="#principles">مبادئنا</a>
      <a href="#pc">للحاسوب</a><a href="#services">خدماتنا</a><a href="#trust">الثقة</a>
      <a href="/en/" lang="en" hreflang="en" title="English">EN</a>
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
    <p class="sub">أربعة عشر تطبيقاً وُلدت في بيتٍ واحد: <b>بلا إعلانات، بلا تتبّع، بلا سحابة</b>. بياناتك تبقى على جهازك، وأكثر التطبيقات يعمل دون اتصالٍ بالإنترنت أصلاً.</p>
    <div class="ctas">
      <a class="btn btn-gold" data-store-dl href="{store['apkUrl']}">⬇ نزّل متجر أمان (APK)</a>
      <a class="btn btn-ghost" href="#apps">تعرف على التطبيقات</a>
    </div>
    <div class="chips">
      <span class="chip"><b>14</b> تطبيقاً</span>
      <span class="chip"><b>0</b> إعلانات</span>
      <span class="chip"><b>0</b> متتبّعات</span>
      <span class="chip"><b>100%</b> عربي أولاً</span>
    </div>
    <div class="orbit" aria-hidden="true"><div class="orbit-track">{orbit_tiles}{orbit_tiles}</div></div>
  </div>
</header>

<section id="principles">
  <div class="wrap">
    <p class="sec-k">مبادئنا</p>
    <h2>الخصوصية عندنا مبدأ، لا إعداد</h2>
    <p class="lead">لا نطلب منك أن تثق بوعودنا — نبني التطبيق بحيث لا يحتاج ثقتك أصلاً.</p>
    <div class="prin">
      <div class="p-card reveal"><div class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 1l22 22M9 9a7 7 0 0 1 10 6M5 12a11 11 0 0 1 2.6-3.4M12 20h.01M8.5 16.5a5 5 0 0 1 5.5-1"/></svg></div>
        <h3>بلا إنترنت حيث يجب</h3><p>الوثائق والتقويم والإشعارات والسِتر: حزمها لا تحمل إذن الإنترنت أصلاً — تحقّق بنفسك من إعدادات النظام.</p></div>
      <div class="p-card reveal"><div class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-3 8-10V5l-8-3-8 3v7c0 7 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg></div>
        <h3>توقيع يُفحص قبل التثبيت</h3><p>متجر أمان يطابق بصمة توقيع كل حزمة مع بصمتها المثبّتة لديه — حزمة مزوّرة لا تمرّ.</p></div>
      <div class="p-card reveal"><div class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="6" width="9" height="14" rx="2"/><rect x="13" y="4" width="9" height="14" rx="2"/><path d="M6.5 17h.01M17.5 15h.01"/></svg></div>
        <h3>ينتشر جهازاً لجهاز</h3><p>المتجر وتطبيقاته تُشارَك بالقرب دون إنترنت — يكفي أن يملكه صديقك ليصلك كل شيء.</p></div>
      <div class="p-card reveal"><div class="ic"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg></div>
        <h3>عربيٌّ أولاً</h3><p>من اليمين إلى اليسار تصميماً لا ترجمةً — بخط المراعي وذوقٍ واحد يجمع العائلة كلها.</p></div>
    </div>
  </div>
</section>

<section id="apps" style="padding-top:20px">
  <div class="wrap">
    <p class="sec-k">العائلة</p>
    <h2>أربعة عشر فرداً، بيتٌ واحد</h2>
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
    <h2>وللحاسوب نصيبه</h2>
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
    <div class="pc reveal" style="margin-top:18px">
      {tile("tayf")}
      <div>
        <h3>طيف لويندوز</h3>
        <p>متصفّح طيف على كروميوم حقيقي — حجب المتعقّبات في المحرّك نفسه، وتنزيل الفيديو من الصفحة، بلا حساب ولا مزامنة.</p>
      </div>
      <div class="pc-btns">
        <a class="btn btn-gold" href="{TAYF_WIN_SETUP}">⬇ المثبّت (Setup)</a>
        <a class="btn btn-ghost" href="{TAYF_WIN_ZIP}">نسخة محمولة (ZIP)</a>
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
      <div class="step reveal"><h3>شاركه من جهازٍ لجهاز</h3><p>مرّر المتجر وتطبيقاته لأهلك وأصدقائك بالمشاركة القريبة أو عبر جسر — بلا إنترنت إطلاقاً.</p></div>
    </div>
  </div>
</section>

<section id="services" style="padding-top:10px">
  <div class="wrap">
    <p class="sec-k">خدماتنا</p>
    <h2>لديك <span style="color:var(--gold)">فكرة</span> تطبيق؟ ننفّذها لك</h2>
    <div class="svc reveal">
      <div class="svc-main">
        <p class="svc-body">تبحث عن جهةٍ تنفّذها؟ نبني المواقع والتطبيقات من الفكرة إلى الإطلاق — والدليل أمامك: هذه العائلة كلها صنعتُنا. أرسل فكرتك، ونعود إليك بخطةٍ وسعرٍ واضحين قبل أي التزام.</p>
        <div class="svc-feats">
          <div class="svc-f"><span>🧩</span>مواقع وتطبيقات ومتاجر وأنظمة خاصة</div>
          <div class="svc-f"><span>🚀</span>تنفيذ كامل: تصميم وبرمجة ونشر</div>
          <div class="svc-f"><span>🤝</span>سعر منافس يُتَّفق عليه قبل البدء</div>
        </div>
        <div class="ctas" style="margin-top:26px">
          <a class="btn btn-ghost svc-cta" href="{WA_REQUEST}" rel="noopener">أرسل فكرتك عبر واتساب</a>
        </div>
      </div>
    </div>
    <div class="svc-strip reveal">
      <p>أمان مشروعٌ مستقل لا يقصد الربح: لا إعلانات، ولا ثمن خفيّ. تطبيقاته كاملة للجميع دوماً، ودعمكم الاختياري يُبقيها كذلك — <b>ستُتاح طرق المساهمة قريباً</b>، لمزيدٍ من مشاريع الخصوصية: شات، تخزين سحابي آمن، VPN…</p>
      <a href="{WA_REPORT}" rel="noopener">واجهتك مشكلة في تطبيق؟ أبلغنا عنها ↲</a>
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
    </div>
    <div class="t-visual" aria-hidden="true">
      {"".join(tile(slug(a["packageName"])) for a in shown)}
    </div>
  </div>
</section>

<footer>
  <div class="wrap f-in">
    <a class="brand" href="#top">{tile("store")} مختبرات أمان</a>
    <div class="f-links">
      <a href="https://wa.me/963943558806" rel="noopener">تواصل واتساب</a>
    </div>
    <p class="f-note">© 2026 مختبرات أمان · Aman Labs — جميع الحقوق محفوظة.</p>
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
    // التغبيش الحي (2026-09-18): الكاتالوغ المنشور يحسم من يظهر ومن يبقى ضباباً — فتبديلُ المالك
    // من لوحة المشرف يصل الموقعَ مع أول تحميل، بلا إعادة بناء. البطاقة الحقيقية تُبنى هنا من
    // الكاتالوغ نفسه؛ وأيقونةُ من كُشف قبل إعادة البناء تكون بلاطةً عامة حتى البناء التالي.
    function esc(s) {{ return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {{ return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]; }}); }}
    function teaserHtml(idx) {{
      return '<article class="card teaser reveal in" data-tz="' + idx + '">' +
        '<div class="card-head"><span class="tile tz"><i></i><b>✦</b></span>' +
        '<div><h3 class="blur">عضوٌ جديد في العائلة</h3><p class="tag">يُكشف عند إطلاقه</p></div></div>' +
        '<p class="sum blur">تطبيقٌ آخر يولد في بيت أمان — بلا إعلانات ولا تتبّع ولا سحابة</p>' +
        '<div class="feats"><span>قريباً</span><span>تابع القناة</span></div>' +
        '<div class="card-foot"><span class="meta">قريباً</span><span class="dl soon">قريباً</span></div></article>';
    }}
    function realHtml(a) {{
      var s = a.packageName.split('.').pop();
      var parts = String(a.nameAr || '').split(' — ');
      var name = parts[0], tag = parts.slice(1).join(' — ');
      var tileHtml = document.getElementById('i-' + s)
        ? '<svg class="tile" viewBox="0 0 108 108" aria-hidden="true"><use href="#i-' + s + '"/></svg>'
        : '<span class="tile tz"><i></i><b>' + esc(Array.from(name.trim())[0] || '•') + '</b></span>';
      var feats = (a.featuresAr || []).slice(0, 3).map(function (f) {{ return '<span>' + esc(f) + '</span>'; }}).join('');
      return '<article class="card reveal in" style="--ac:' + esc(a.accentHex || '#E0A32E') + '" data-pkg="' + esc(a.packageName) + '">' +
        '<div class="card-head">' + tileHtml + '<div><h3>' + esc(name) + '</h3><p class="tag">' + esc(tag) + '</p></div></div>' +
        '<p class="sum">' + esc(a.summaryAr || '') + '</p><div class="feats">' + feats + '</div>' +
        '<div class="card-foot"><span class="meta"><b data-v>' + esc(a.versionName || '') + '</b> · <span data-s>' + mb(a.sizeBytes || 0) + '</span></span>' +
        '<a class="dl" data-dl href="' + esc(a.apkUrl) + '" rel="nofollow">تنزيل APK</a></div></article>';
    }}
    function applyHidden(c) {{
      c.apps.forEach(function (a) {{
        if (/\\.store$/.test(a.packageName)) return;
        var real = document.querySelector('.card[data-pkg="' + a.packageName + '"]');
        var tz = document.querySelector('.card[data-tz="' + a.index + '"]');
        if (a.hidden && real) real.outerHTML = teaserHtml(a.index);
        else if (!a.hidden && tz) tz.outerHTML = realHtml(a);
      }});
    }}
    // مرآة كلاودفلير (سوريا بلا VPN) — لا احتياط خارجي: لا يُذكر أي مضيف آخر في الصفحة
    function useCat(c) {{
      var m = {{}};
      c.apps.forEach(function (a) {{ m[a.packageName] = {{ v: a.versionName, s: a.sizeBytes, u: a.apkUrl }}; }});
      try {{ applyHidden(c); }} catch (e) {{}}
      apply(m);
    }}
    fetch('https://dl.amanlabs.app/catalog.json', {{ cache: 'no-store' }})
      .then(function (r) {{ if (!r.ok) throw 0; return r.json(); }})
      .then(useCat)
      .catch(function () {{}});
    // عدّاد التنزيلات (2026-09-25): تُحصيه المرآة لكل عضو — يُلحق بسطر الإصدار والحجم في كل بطاقة
    function fmtCount(n) {{ n = +n || 0; if (n >= 1e6) return (Math.round(n / 1e5) / 10) + 'M'; if (n >= 1e3) return (Math.round(n / 100) / 10) + 'k'; return String(n); }}
    function statsKey(pkg) {{ var t = pkg.split('.').pop().toLowerCase(); return t === 'store' ? 'amanstore' : t; }}
    var DL_ICON = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>';
    function applyStats(st) {{
      var d = (st && st.downloads) || {{}};
      document.querySelectorAll('[data-pkg]').forEach(function (el) {{
        var n = d[statsKey(el.getAttribute('data-pkg'))];
        if (!n) return;
        var tile = el.querySelector('.tile');
        if (!tile || tile.parentNode.classList.contains('twrap')) return;
        // كبسولة العدّاد على زاوية الأيقونة — كما في المتجر
        var wrap = document.createElement('span'); wrap.className = 'twrap';
        tile.parentNode.insertBefore(wrap, tile); wrap.appendChild(tile);
        var s = document.createElement('span'); s.className = 'tcount'; s.title = 'عدد التنزيلات';
        s.innerHTML = DL_ICON + '<b>' + fmtCount(n) + '</b><small>تنزيل</small>';
        wrap.appendChild(s);
      }});
    }}
    fetch('https://dl.amanlabs.app/stats.json', {{ cache: 'no-store' }})
      .then(function (r) {{ if (!r.ok) throw 0; return r.json(); }})
      .then(applyStats)
      .catch(function () {{}});
  }})();
</script>
</body>
</html>
'''

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8").write(HTML)
print("site written:", OUT, len(HTML), "chars")

# ═══ الصفحة الإنكليزية: القالب العربي نفسه مع تبديل النصوص والاتجاه ═══
T = [
    ('<html lang="ar" dir="rtl">', '<html lang="en" dir="ltr">'),
    ('<title>مختبرات أمان — عائلة تطبيقات الخصوصية العربية</title>', '<title>Aman Labs — privacy-first Arabic apps</title>'),
    ('<meta property="og:title" content="مختبرات أمان — عائلة تطبيقات الخصوصية العربية">', '<meta property="og:title" content="Aman Labs — privacy-first Arabic apps">'),
    ('<meta property="og:url" content="https://amanlabs.app/">', '<meta property="og:url" content="https://amanlabs.app/en/">'),
    ('<link rel="canonical" href="https://amanlabs.app/">', '<link rel="canonical" href="https://amanlabs.app/en/">'),
    ('<a href="/en/" lang="en" hreflang="en" title="English">EN</a>', '<a href="/" lang="ar" hreflang="ar" title="العربية">عربي</a>'),
    ('مختبرات أمان</a>', 'Aman Labs</a>'),
    ('<a href="#apps">التطبيقات</a><a href="#principles">مبادئنا</a>', '<a href="#apps">Apps</a><a href="#principles">Principles</a>'),
    ('<a href="#pc">للحاسوب</a><a href="#services">خدماتنا</a><a href="#trust">الثقة</a>', '<a href="#pc">Desktop</a><a href="#services">Services</a><a href="#trust">Trust</a>'),
    ('>نزّل المتجر</a>', '>Get the store</a>'),
    ('<p class="kicker">عائلة أمان · Aman Labs</p>', '<p class="kicker">Aman Labs · عائلة أمان</p>'),
    ('<h1>تطبيقاتٌ عربيةٌ تعمل لك،<br>لا عليك.</h1>', '<h1>Arabic apps that work for you,<br>not on you.</h1>'),
    ('<p class="sub">أربعة عشر تطبيقاً وُلدت في بيتٍ واحد: <b>بلا إعلانات، بلا تتبّع، بلا سحابة</b>. بياناتك تبقى على جهازك، وأكثر التطبيقات يعمل دون اتصالٍ بالإنترنت أصلاً.</p>',
     '<p class="sub">Fourteen apps from one house: <b>no ads, no tracking, no cloud</b>. Your data stays on your phone, and most of the apps do not even have an internet permission.</p>'),
    ('>⬇ نزّل متجر أمان (APK)</a>', '>⬇ Download Aman Store (APK)</a>'),
    ('>تعرف على التطبيقات</a>', '>Meet the apps</a>'),
    ('<span class="chip"><b>14</b> تطبيقاً</span>', '<span class="chip"><b>14</b> apps</span>'),
    ('<span class="chip"><b>0</b> إعلانات</span>', '<span class="chip"><b>0</b> ads</span>'),
    ('<span class="chip"><b>0</b> متتبّعات</span>', '<span class="chip"><b>0</b> trackers</span>'),
    ('<span class="chip"><b>100%</b> عربي أولاً</span>', '<span class="chip"><b>100%</b> Arabic first</span>'),
    ('<p class="sec-k">مبادئنا</p>', '<p class="sec-k">Principles</p>'),
    ('<h2>الخصوصية عندنا مبدأ، لا إعداد</h2>', '<h2>Privacy is a principle here, not a setting</h2>'),
    ('<p class="lead">لا نطلب منك أن تثق بوعودنا — نبني التطبيق بحيث لا يحتاج ثقتك أصلاً.</p>', '<p class="lead">We do not ask you to trust a promise. We build the app so that it does not need your trust in the first place.</p>'),
    ('<h3>بلا إنترنت حيث يجب</h3><p>الوثائق والتقويم والإشعارات والسِتر: حزمها لا تحمل إذن الإنترنت أصلاً — تحقّق بنفسك من إعدادات النظام.</p>',
     '<h3>No internet where it matters</h3><p>Documents, calendar, notifications, photo vault: their packages carry no internet permission at all. Check it yourself in system settings.</p>'),
    ('<h3>توقيع يُفحص قبل التثبيت</h3><p>متجر أمان يطابق بصمة توقيع كل حزمة مع بصمتها المثبّتة لديه — حزمة مزوّرة لا تمرّ.</p>',
     '<h3>Signature checked before install</h3><p>Aman Store compares every package\'s signing fingerprint with the one pinned in its catalog. A forged package does not get through.</p>'),
    ('<h3>ينتشر جهازاً لجهاز</h3><p>المتجر وتطبيقاته تُشارَك بالقرب دون إنترنت — يكفي أن يملكه صديقك ليصلك كل شيء.</p>',
     '<h3>Spreads phone to phone</h3><p>The store and its apps can be shared nearby without internet. If a friend has it, you can have everything.</p>'),
    ('<h3>عربيٌّ أولاً</h3><p>من اليمين إلى اليسار تصميماً لا ترجمةً — بخط المراعي وذوقٍ واحد يجمع العائلة كلها.</p>',
     '<h3>Arabic first</h3><p>Designed right-to-left, not translated afterwards, in the Almarai typeface and one visual language across the whole family.</p>'),
    ('<p class="sec-k">العائلة</p>', '<p class="sec-k">The family</p>'),
    ('<h2>أربعة عشر فرداً، بيتٌ واحد</h2>', '<h2>Fourteen members, one house</h2>'),
    ('<p class="lead">كل تطبيقٍ يسدّ حاجةً يومية حقيقية — ويشارك إخوته المبدأ نفسه: بياناتك ملكك وحدك.</p>', '<p class="lead">Each app covers a real daily need, and shares the same rule with its siblings: your data belongs to you alone.</p>'),
    ('<h3>متجر أمان <span class="en">· Aman Store</span></h3>', '<h3>Aman Store <span class="en">· متجر أمان</span></h3>'),
    ('>⬇ تنزيل المتجر</a>', '>⬇ Download the store</a>'),
    ('<span class="meta">الإصدار <b data-v>', '<span class="meta">Version <b data-v>'),
    (' · أندرويد 7+</span>', ' · Android 7+</span>'),
    ('<p class="sec-k">للحاسوب</p>', '<p class="sec-k">Desktop</p>'),
    ('<h2>وللحاسوب نصيبه</h2>', '<h2>The desktop gets its share</h2>'),
    ('<h3>جسر لويندوز</h3>', '<h3>Jisr for Windows</h3>'),
    ('<p>انقل الملفات بين هاتفك وحاسوبك عبر شبكتك المحلية وحدها — بلا كابل ولا سحابة ولا حدود حجم.</p>', '<p>Move files between your phone and your computer over your local network only. No cable, no cloud, no size limit.</p>'),
    ('<h3>طيف لويندوز</h3>', '<h3>Tayf for Windows</h3>'),
    ('<p>متصفّح طيف على كروميوم حقيقي — حجب المتعقّبات في المحرّك نفسه، وتنزيل الفيديو من الصفحة، بلا حساب ولا مزامنة.</p>', '<p>Tayf on real Chromium: tracker blocking inside the engine, video download from the page, no account and no sync.</p>'),
    ('>⬇ المثبّت (Setup)</a>', '>⬇ Installer (Setup)</a>'),
    ('>نسخة محمولة (ZIP)</a>', '>Portable (ZIP)</a>'),
    ('<span class="pc-note">ويندوز 10/11 · 64bit</span>', '<span class="pc-note">Windows 10/11 · 64-bit</span>'),
    ('<p class="sec-k">كيف يصلك أمان؟</p>', '<p class="sec-k">How to get it</p>'),
    ('<h2>ثلاث خطوات، ثم لا حاجة للإنترنت</h2>', '<h2>Three steps, then no internet needed</h2>'),
    ('<h3>نزّل متجر أمان</h3><p>ملف APK واحد من هذه الصفحة — ثبّته واسمح بمصادر التثبيت حين يسألك أندرويد.</p>', '<h3>Download Aman Store</h3><p>One APK from this page. Install it and allow this source when Android asks.</p>'),
    ('<h3>ثبّت ما تحب</h3><p>تصفح العائلة داخل المتجر وثبّت بنقرة — المتجر يفحص توقيع كل حزمة قبل تثبيتها.</p>', '<h3>Install what you like</h3><p>Browse the family inside the store and install with one tap. The store verifies each package\'s signature first.</p>'),
    ('<h3>شاركه من جهازٍ لجهاز</h3><p>مرّر المتجر وتطبيقاته لأهلك وأصدقائك بالمشاركة القريبة أو عبر جسر — بلا إنترنت إطلاقاً.</p>', '<h3>Pass it on</h3><p>Hand the store and its apps to family and friends with nearby sharing or through Jisr. No internet involved.</p>'),
    ('<p class="sec-k">خدماتنا</p>', '<p class="sec-k">Services</p>'),
    ('<h2>لديك <span style="color:var(--gold)">فكرة</span> تطبيق؟ ننفّذها لك</h2>', '<h2>Have an <span style="color:var(--gold)">idea</span> for an app? We build it</h2>'),
    ('<p class="svc-body">تبحث عن جهةٍ تنفّذها؟ نبني المواقع والتطبيقات من الفكرة إلى الإطلاق — والدليل أمامك: هذه العائلة كلها صنعتُنا. أرسل فكرتك، ونعود إليك بخطةٍ وسعرٍ واضحين قبل أي التزام.</p>',
     '<p class="svc-body">Looking for someone to build it? We take websites and apps from idea to launch, and the proof is on this page: this whole family is our work. Send the idea and you get a plan and a clear price before any commitment.</p>'),
    ('<div class="svc-f"><span>🧩</span>مواقع وتطبيقات ومتاجر وأنظمة خاصة</div>', '<div class="svc-f"><span>🧩</span>Websites, apps, stores and custom systems</div>'),
    ('<div class="svc-f"><span>🚀</span>تنفيذ كامل: تصميم وبرمجة ونشر</div>', '<div class="svc-f"><span>🚀</span>End to end: design, code, release</div>'),
    ('<div class="svc-f"><span>🤝</span>سعر منافس يُتَّفق عليه قبل البدء</div>', '<div class="svc-f"><span>🤝</span>A fair price agreed before work starts</div>'),
    ('>أرسل فكرتك عبر واتساب</a>', '>Send your idea on WhatsApp</a>'),
    ('<p>أمان مشروعٌ مستقل لا يقصد الربح: لا إعلانات، ولا ثمن خفيّ. تطبيقاته كاملة للجميع دوماً، ودعمكم الاختياري يُبقيها كذلك — <b>ستُتاح طرق المساهمة قريباً</b>، لمزيدٍ من مشاريع الخصوصية: شات، تخزين سحابي آمن، VPN…</p>',
     '<p>Aman is an independent, non-commercial project: no ads, no hidden price. The apps are complete for everyone, always, and optional support keeps them that way. <b>Ways to contribute are coming</b>, for more privacy projects: chat, safe cloud storage, VPN…</p>'),
    ('>واجهتك مشكلة في تطبيق؟ أبلغنا عنها ↲</a>', '>Something broke in an app? Tell us ↲</a>'),
    ('<p class="sec-k">الثقة تُبنى بالهندسة</p>', '<p class="sec-k">Trust is engineered</p>'),
    ('<h2>شفافيةٌ يمكنك التحقق منها بنفسك</h2>', '<h2>Transparency you can verify yourself</h2>'),
    ('<b>بصمات توقيع معلنة ومثبّتة</b><p>بصمة SHA-256 لتوقيع كل تطبيق منشورة في كاتالوغ عام، والمتجر يرفض أي حزمة تخالفها.</p>', '<b>Published, pinned signing fingerprints</b><p>The SHA-256 of each app\'s signing certificate is in a public catalog, and the store rejects any package that does not match.</p>'),
    ('<b>بصمة لكل ملف</b><p>لكل حزمة sha256 معلنة — تستطيع التحقق من أي ملف نزّلته بنفسك قبل تثبيته.</p>', '<b>A hash for every file</b><p>Every package has a published sha256, so you can check any download yourself before installing.</p>'),
    ('<b>حارس بناءٍ صارم</b><p>التطبيقات الحساسة تُبنى بحارسٍ يفشل البناء كله إن تسلّلت أي مكتبة شبكية أو إذنٌ غير مبرَّر.</p>', '<b>A strict build guard</b><p>Sensitive apps are built with a guard that fails the whole build if a networking library or an unjustified permission slips in.</p>'),
    ('<b>بياناتك تغادر معك فقط</b><p>نسخ احتياطي موحّد مشفّر بمفتاحٍ تحفظه أنت — لا حسابات ولا خوادم ولا «مزامنة» خفية.</p>', '<b>Your data leaves only with you</b><p>One encrypted family backup, unlocked by a key you keep. No accounts, no servers, no hidden "sync".</p>'),
    ('>تواصل واتساب</a>', '>WhatsApp</a>'),
    ('<p class="f-note">© 2026 مختبرات أمان · Aman Labs — جميع الحقوق محفوظة.</p>', '<p class="f-note">© 2026 Aman Labs · مختبرات أمان. All rights reserved.</p>'),
    # سكربت البطاقات الحي
    ("<h3 class=\"blur\">عضوٌ جديد في العائلة</h3><p class=\"tag\">يُكشف عند إطلاقه</p>", "<h3 class=\"blur\">A new family member</h3><p class=\"tag\">Revealed at launch</p>"),
    ("<p class=\"sum blur\">تطبيقٌ آخر يولد في بيت أمان — بلا إعلانات ولا تتبّع ولا سحابة</p>", "<p class=\"sum blur\">Another app born in the Aman house — no ads, no tracking, no cloud</p>"),
    ("<div class=\"feats\"><span>قريباً</span><span>تابع القناة</span></div>", "<div class=\"feats\"><span>Soon</span><span>Stay tuned</span></div>"),
    ("<span class=\"meta\">قريباً</span><span class=\"dl soon\">قريباً</span>", "<span class=\"meta\">Soon</span><span class=\"dl soon\">Soon</span>"),
    ("String(a.nameAr || '')", "String(a.nameEn || a.nameAr || '')"),
    ("(a.featuresAr || [])", "(a.featuresEn || a.featuresAr || [])"),
    ("esc(a.summaryAr || '')", "esc(a.summaryEn || a.summaryAr || '')"),
    ('rel="nofollow">تنزيل APK</a>', 'rel="nofollow">Download APK</a>'),
    ("s.title = 'عدد التنزيلات';", "s.title = 'downloads';"),
    ("'<small>تنزيل</small>'", "'<small>downloads</small>'"),
]
HTML_EN = HTML
HTML_EN = HTML_EN.replace(CARDS, CARDS_EN, 1)
HTML_EN = HTML_EN.replace(store['descriptionAr'], store['descriptionEn'], 1)
HTML_EN = re.sub(r'<meta name="description" content="[^"]*">',
                 '<meta name="description" content="Fourteen Arabic-first Android apps with no ads, no tracking and no cloud. Your data stays on your phone; most apps work without internet. Free, signed, verifiable.">', HTML_EN, 1)
HTML_EN = re.sub(r'<meta property="og:description" content="[^"]*">',
                 '<meta property="og:description" content="Fourteen Arabic-first apps: no ads, no tracking, no cloud. Most work without internet.">', HTML_EN, 1)
missing = []
for a_, b_ in T:
    if a_ not in HTML_EN:
        missing.append(a_[:60]); continue
    HTML_EN = HTML_EN.replace(a_, b_)
if missing:
    print("EN: untranslated fragments:", missing)
rest = re.findall(r'>[^<{}]*[\u0600-\u06FF][^<]*<', HTML_EN.split("<script>")[0].split("</style>")[-1])
rest = [r for r in rest if "متجر أمان" not in r and "عائلة أمان" not in r and "عربي" not in r and "مختبرات" not in r]
if rest:
    print("EN: Arabic text still visible:", rest[:8])
en_dir = os.path.join(os.path.dirname(OUT), "en")
os.makedirs(en_dir, exist_ok=True)
io.open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8").write(HTML_EN)
print("site written:", os.path.join(en_dir, "index.html"), len(HTML_EN), "chars")
# نظام ملفات ويندوز لا يفرّق EN/en فلا مجلدَ بديل؛ GitHub Pages يخدم 404.html لأي مسارٍ مفقود،
# ومنها نحوّل /EN و/En وأشباهها إلى /en/ بالجافاسكربت.
io.open(os.path.join(os.path.dirname(OUT), "404.html"), "w", encoding="utf-8").write(
    '<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Aman Labs</title>'
    '<script>(function(){var p=location.pathname.toLowerCase();'
    r'if(/^\/en\/?$/.test(p)){location.replace("/en/");}else{location.replace("/");}})();</script>'
    '</head><body><a href="/">amanlabs.app</a></body></html>')

# amanlabs.app/store — رابط ثابت للطباعة ورموز QR: يوجّه دوماً لأحدث APK للمتجر من الكاتالوغ
store_dir = os.path.join(os.path.dirname(OUT), "store")
os.makedirs(store_dir, exist_ok=True)
io.open(os.path.join(store_dir, "index.html"), "w", encoding="utf-8").write(
    f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<title>تنزيل متجر أمان</title>
<meta http-equiv="refresh" content="0;url={store['apkUrl']}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{{font-family:sans-serif;background:#0B0E15;color:#F2EDE3;display:grid;place-items:center;min-height:100vh;text-align:center}}a{{color:#E0A32E}}</style>
</head><body><p>يبدأ تنزيل متجر أمان الآن…<br><a href="{store['apkUrl']}">اضغط هنا إن لم يبدأ تلقائياً</a></p>
<script>location.replace({json.dumps(store['apkUrl'])});</script></body></html>''')
print("store redirect written ->", store["apkUrl"])
