# -*- coding: utf-8 -*-
# مولّد «مقترحات تطوير واجهات متجر أمان» — النسخة ٣: «الزجاج المعشّق».
# ورقة قرار محلية قبل التنفيذ. الأيقونات تُضمَّن <img> بملفاتها الأصلية كاملةً
# (خلفياتها هي اللوغو — ثابت المالك)، والليل باردٌ أزرق الميل، والزوايا شبه حادة،
# ولا ذهب مطموساً في الأزرار — خطٌّ شعري ونصٌّ فقط.
import io, os

ROOT = r"D:\Aman Labs\Ready"
OUT = os.path.join(ROOT, "مقترحات-واجهات-المتجر.html")

# (المفتاح، الاسم، السطر، الصبغة)
M = {
 "store":      ("متجر أمان",  "تطبيقات العائلة وتحديثاتها في مكان واحد", "#E0A32E"),
 "kalamboard": ("كلام بورد",  "اكتب بحريةٍ — ولا حرف يغادر جهازك",       "#E0A32E"),
 "mihrab":     ("محراب",      "الأذان في وقته أينما كنت — دون إنترنت",    "#7C89CF"),
 "album":      ("ألبوم",      "جِد أي صورة بلمح البصر، وأخفِ ما تشاء",    "#2A6FB0"),
 "ruznama":    ("رزنامة",     "مواعيدك ودعواتك دون حساب",                "#235C34"),
 "hisn":       ("حصن",        "كلمة سرّ واحدة تحفظ كل كلمات سرّك",        "#C4764E"),
 "wathaiq":    ("وَثائق",     "أوراقك مشفّرة وتذكيرٌ قبل انتهائها",        "#A98A5C"),
 "jisr":       ("جسر",        "شارك ملفات ضخمة بثوانٍ — دون إنترنت",      "#5C7185"),
 "daftar":     ("دفتر",       "اقتنص أفكارك قبل أن تطير — وذكّر نفسك",    "#3FC0C4"),
 "sijil":      ("سِجِلّ",     "كل إشعارٍ مسحته بالخطأ… تجده هنا",         "#E5A21E"),
 "jezdan":     ("جزدان",      "اعرف أين تذهب نقودك — بأي عملة",          "#97C98B"),
 "diwan":      ("ديوان",      "روّض فوضى الملفات وجِد أي شيءٍ بسرعة",     "#7A4A72"),
 "sitr":       ("سِتر",       "ما تخفيه لا يراه سواك",                   "#9D85C4"),
 "qamariya":   ("قمرية",      "اعرفي أيامك قادماً — وسرّك يبقى لك",       "#D97C93"),
}

def tile(key, size, cls=""):
    # كل أيقونة بملفها الأصلي كاملاً — سماؤها الملوّنة هي اللوغو (ثابت المالك 2026-09-03)
    return ('<img class="tile %s" style="width:%dpx;height:%dpx" '
            'src="AmanWeb/tools/site_icons/%s.svg" alt="">') % (cls, size, size, key)

def action(kind):
    if kind == "open":   return '<span class="act">فتح</span>'
    if kind == "get":    return '<span class="act">تنزيل</span>'
    if kind == "update": return '<span class="act goldln">تحديث</span>'
    return ""

def grow(key, kind, fav=False, self_row=False):
    # نفس ارتفاع صف اليوم — لا زيادة بكسل (ثابت المالك)؛ الزجاج ثوبٌ لا قياس
    name, sub, _ = M[key]
    petal = '<span class="petal %s">✿</span>' % ("on" if fav else "")
    acts = "" if self_row else '<div class="racts">%s%s</div>' % (action(kind), petal)
    return ('<div class="g-row %s">%s<div class="rtx"><div class="rname">%s</div>'
            '<div class="rsub">%s</div>%s</div></div>') % (
        "selfrow" if self_row else "", tile(key, 40, "sq"), name, sub, acts)

def arc():
    # «قوس معشّق»: خمسُ سماوات العائلة كقطعِ زجاجٍ يفصلها رصاصُ الليل
    panes = ["#E0A32E", "#3FC0C4", "#D97C93", "#7C89CF", "#97C98B"]
    return '<div class="arc">%s</div>' % "".join(
        '<i style="background:linear-gradient(180deg,%s,%scc)"></i>' % (c, c) for c in panes)

def navbar(active):
    labels = ["التطبيقات", "الدعم", "المبادئ", "الإعدادات"]
    icons = ["▦", "♡", "🛡", "⚙"]
    items = "".join('<span class="nav %s"><i>%s</i>%s</span>' % ("on" if i == a else "", icons[i], labels[i]) for i, a in ((j, active) for j in range(4)))
    return '<div class="navbar">%s</div>' % items

def phone(inner, label):
    return ('<figure class="phwrap"><div class="phone"><div class="amb"></div>'
            '<div class="ph-in"><div class="sbar"><span>9:41</span><span>●●●</span></div>%s</div>'
            '</div><figcaption>%s</figcaption></figure>') % (inner, label)

def topbar():
    return ('<div class="tb">%s<span class="tbt">متجر أمان</span>'
            '<span class="tbi">✈ ⤴</span></div>%s') % (tile("store", 24, "glow"), arc())

def mock_home_updates():
    minis = "".join('<div class="mini">%s<span>%s</span></div>' % (tile(k, 32, "sq"), M[k][0]) for k in ["mihrab", "daftar", "jezdan"])
    hero = ('<div class="hero"><div class="hero-n">3</div><div class="hero-tx">'
            '<div class="hero-t">تحديثات بانتظارك</div><div class="hero-s">محراب · دفتر · جزدان</div></div>'
            '<span class="act goldln big">حدّث الكل</span></div>'
            '<div class="minirow">%s</div>') % minis
    rows = [grow("store", "", self_row=True),
            grow("kalamboard", "open", fav=True),
            grow("mihrab", "update"),
            grow("sijil", "open"),
            grow("hisn", "get")]
    inner = ('%s<div class="search">⌕ &nbsp;ابحث في العائلة…</div>%s'
             '<div class="sech">كل العائلة</div><div class="list">%s</div>%s') % (
        topbar(), hero, "".join(rows), navbar(0))
    return phone(inner, "الرئيسية — «التحديثات أولاً» المعتمدة، زجاجاً: الرقم والزر ذهبُ خطٍّ لا طلاء")

def mock_home_featured():
    name, sub, acc = M["sitr"]
    feat = ('<div class="featured" style="--fa:%s"><div class="feat-tag">عضو الأسبوع</div>'
            '<div class="feat-row">%s<div><div class="feat-n">%s</div>'
            '<div class="feat-s">ضعي صوركِ وصور صديقاتكِ وعائلتكِ في مأمنٍ لا تبلغه عين — حتى لو سُرق هاتفكِ.</div></div></div>'
            '<span class="act accln" style="--fa:%s">تنزيل</span>'
            '<div class="dots"><b></b><i></i><i></i></div></div>') % (acc, tile("sitr", 46, "sq"), name, acc)
    rows = [grow("album", "get"),
            grow("wathaiq", "get"),
            grow("diwan", "open")]
    inner = ('%s<div class="search">⌕ &nbsp;ابحث في العائلة…</div>%s'
             '<div class="list">%s</div>%s') % (topbar(), feat, "".join(rows), navbar(0))
    return phone(inner, "«عضو الأسبوع» المعتمدة — سِتر بخطاب المحجبات، إطارُ زجاجٍ بصبغة العضو (قمرية مستثناة)")

def mock_detail():
    name, sub, acc = M["mihrab"]
    # صفوفٌ شبحية خلف التعتيم — النافذة تطفو فوق متجرٍ حي لا فراغٍ أسود
    ghost = (grow("store", "", self_row=True) + grow("kalamboard", "open") + grow("mihrab", "update"))
    inner = ('%s<div class="list">%s</div><div class="dim"></div>'
             '<div class="sheet"><div class="grab"></div>'
             '<div class="dpane" style="--fa:%s">%s<div><div class="dname">%s</div>'
             '<div class="dchips"><span>النسخة 1.0.25</span><span>4.2MB</span><span>Android 8+</span></div></div></div>'
             '<div class="dsum">%s. مواقيت دقيقة بلا موقعٍ مرسل، وأذانٌ يعمل والجهاز مقفل.</div>'
             '<div class="feats"><span>مواقيت بلا إنترنت</span><span>أذان والشاشة مقفلة</span><span>بلا حساب</span></div>'
             '<span class="acq" style="--fa:%s">تنزيل التطبيق</span>'
             '<span class="acq ghost">إغلاق</span>'
             '</div>') % (topbar(), ghost, acc, tile("mihrab", 56, "sq"), name, sub, acc)
    return phone(inner, "نافذة التفاصيل — لوحُ زجاجٍ بصبغة العضو، وزرُ اقتناءٍ زجاجيٌّ لا مطموس")

def mock_support():
    doors = [
        ("♡", "ادعم العائلة", "طرق الدعم والمساهمة", "#D97C93"),
        ("💡", "لديك فكرة تطبيق؟", "اطلب مشروعك — قد يصير عضو العائلة", "#E0A32E"),
        ("⚑", "أبلغ عن مشكلة", "أخبرنا وسنصلحها بإذن الله", "#97C98B"),
        ("✈", "قناة التلغرام", "آخر الأخبار والإصدارات", "#2AABEE"),
    ]
    rows = "".join(
        ('<div class="door" style="--fa:%s"><span class="dico">%s</span>'
         '<div class="rtx"><div class="rname">%s</div><div class="rsub">%s</div></div>'
         '<span class="chev">‹</span></div>') % (c, ic, t, s) for ic, t, s, c in doors)
    inner = ('%s<div class="sech pad">الدعم</div><div class="list">%s</div>%s') % (topbar(), rows, navbar(1))
    return phone(inner, "الدعم — تلغرام صار آخر الأبواب كما أمرت (نُفِّذ فعلاً في 1.24.26)")

HTML = u"""<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مقترحات واجهات متجر أمان — الزجاج المعشّق</title>
<style>
@font-face{font-family:Almarai;src:url('Sijil/app/src/main/res/font/almarai_regular.ttf');font-weight:400}
@font-face{font-family:Almarai;src:url('Sijil/app/src/main/res/font/almarai_bold.ttf');font-weight:700}
@font-face{font-family:Almarai;src:url('Sijil/app/src/main/res/font/almarai_extrabold.ttf');font-weight:800}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#101219;color:#DDE1EA;font-family:Almarai,'Segoe UI',Tahoma,Arial,sans-serif;line-height:1.75}
.wrap{max-width:1180px;margin:0 auto;padding:34px 26px 70px}
header.top{display:flex;align-items:flex-start;gap:18px;flex-wrap:wrap;border-bottom:1px solid #272d3a;padding-bottom:22px;margin-bottom:26px}
h1{font-size:31px;font-weight:800;color:#F0F3FA}
h1 b{color:#E0A32E}
.sub{color:#98A1B3;font-size:14.5px;margin-top:6px}
.toggle{margin-inline-start:auto;background:#1B2029;border:1px solid #3A4356;color:#E4CE92;border-radius:8px;padding:9px 18px;font-family:inherit;font-size:14px;cursor:pointer}
.toggle:hover{background:#222836}
section{margin-top:44px}
h2{font-size:22px;font-weight:800;color:#F0CD7A}
.tagline{color:#A9B2C4;font-size:15px;margin:6px 0 16px;max-width:900px}
.contract{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.contract span{background:#181C25;border:1px solid #2C3342;color:#C7CFDE;border-radius:7px;padding:6px 13px;font-size:13px}
.contract.new span{border-color:#5a4a1f;background:#1f1c14;color:#EBD9A6}
.subh{color:#B9C2D4;font-size:14.5px;font-weight:700;margin-top:18px}
.cols{display:flex;gap:26px;flex-wrap:wrap;align-items:flex-start;margin-top:16px}
.notes{flex:1;min-width:300px}
.notes h3{color:#CBD5E8;font-size:16px;margin:14px 0 6px}
.notes ul{padding-inline-start:20px;color:#C2CAD9;font-size:14.5px}
.notes li{margin:5px 0}
.meta{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.meta span{border-radius:7px;padding:5px 12px;font-size:12.5px;border:1px solid transparent}
.m-imp{background:#241f10;color:#F0CD7A;border-color:#4a3a1c}
.m-cost{background:#16201d;color:#A9D3BE;border-color:#254237}
.m-risk{background:#211418;color:#E3A5B2;border-color:#43222c}
.reco{background:linear-gradient(160deg,#181D28,#141822);border:1px solid #3A4358;border-radius:10px;padding:22px 24px;margin-top:20px}
.reco b{color:#F0CD7A}
footer{margin-top:60px;border-top:1px solid #272d3a;padding-top:18px;color:#7E8798;font-size:13px;text-align:center}
/* ————— الهواتف ————— */
.phones{display:flex;gap:24px;flex-wrap:wrap;margin-top:8px}
.phwrap{display:inline-block;vertical-align:top}
.phwrap figcaption{max-width:292px;color:#8E96A8;font-size:12.8px;margin-top:9px;line-height:1.6;text-align:center}
.phone{width:292px;height:566px;border-radius:30px;border:7px solid #05060a;outline:1px solid #39404F;overflow:hidden;position:relative;direction:rtl;font-size:12px;color:var(--mink);background:var(--mbg)}
.ph-in{position:relative;z-index:2;height:100%;display:flex;flex-direction:column}
/* بقعُ ضوء العائلة خلف الزجاج — بلا ضوءٍ خلفه لا يكون الزجاجُ زجاجاً */
.amb{position:absolute;inset:0;z-index:1;filter:blur(30px);opacity:var(--amb-op);
 background:
  radial-gradient(170px 170px at 82% 5%, #E0A32Ecc, transparent 70%),
  radial-gradient(190px 190px at 6% 24%, #7C89CFaa, transparent 70%),
  radial-gradient(180px 180px at 90% 52%, #3FC0C499, transparent 70%),
  radial-gradient(170px 170px at 10% 80%, #D97C9399, transparent 70%),
  radial-gradient(150px 150px at 68% 97%, #97C98B88, transparent 70%)}
:root{--mbg:#10131B;--mink:#ECEFF5;--msub:#A6AEBF;--glass:rgba(255,255,255,.055);--glassbrd:rgba(255,255,255,.14);--goldtx:#E8C46A;--amb-op:.75;--seln:rgba(255,255,255,.09)}
body.mock-light{--mbg:#F6F1E7;--mink:#241F18;--msub:#6E6350;--glass:rgba(255,255,255,.6);--glassbrd:rgba(90,75,45,.18);--goldtx:#8A6A30;--amb-op:.34;--seln:rgba(255,255,255,.85)}
.sbar{display:flex;justify-content:space-between;padding:7px 16px 2px;font-size:10px;color:var(--msub)}
.tb{display:flex;align-items:center;gap:8px;padding:9px 14px 7px}
.tbt{font-weight:800;font-size:15px;flex:1}
.tbi{color:var(--goldtx);letter-spacing:4px;font-size:12px}
.tile.glow{filter:drop-shadow(0 0 9px rgba(224,163,46,.55))}
/* القوس المعشّق: قطعُ زجاجٍ يفصلها رصاص */
.arc{display:flex;gap:2px;height:6px;background:#00000066;padding:0 0}
.arc i{flex:1;opacity:.8}
body.mock-light .arc{background:#3a2f1f22}
.list{padding:7px 10px;flex:1;overflow:hidden}
.g-row,.door{display:flex;gap:9px;align-items:center;padding:7px 9px;margin-bottom:5px;border-radius:6px;
 background:var(--glass);border:1px solid var(--glassbrd);backdrop-filter:blur(13px);-webkit-backdrop-filter:blur(13px)}
.g-row.selfrow{border-color:rgba(224,163,46,.5)}
.tile{border-radius:8px;flex:none}
.tile.sq{border-radius:8px}
.rtx{flex:1;min-width:0}
.rname{font-weight:700;font-size:12.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--mink)}
.rsub{color:var(--msub);font-size:10.6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:2px}
.racts{display:flex;gap:7px;align-items:center;margin-top:3px}
.act{border:1px solid var(--glassbrd);background:rgba(255,255,255,.03);color:var(--mink);border-radius:5px;padding:2px 12px;font-size:10.5px;font-weight:700}
.act.goldln{border-color:rgba(224,163,46,.7);color:var(--goldtx);background:transparent}
.act.goldln.big{padding:5px 14px;font-size:11px}
.act.accln{border-color:color-mix(in srgb, var(--fa) 65%, transparent);color:var(--mink);display:inline-block;margin-top:8px;padding:4px 16px}
.petal{color:var(--msub);font-size:12px}
.petal.on{color:var(--goldtx)}
.search{margin:7px 12px 3px;background:var(--glass);border:1px solid var(--glassbrd);backdrop-filter:blur(13px);border-radius:6px;padding:8px 13px;color:var(--msub);font-size:12px}
.sech{color:var(--goldtx);font-weight:700;font-size:11.5px;padding:8px 16px 2px}
.sech.pad{font-size:14px;padding-top:12px}
.hero{margin:8px 12px 2px;border-radius:6px;padding:11px 13px;display:flex;align-items:center;gap:12px;
 background:var(--glass);border:1px solid var(--glassbrd);backdrop-filter:blur(13px)}
.hero-n{font-size:30px;font-weight:800;color:var(--goldtx)}
.hero-tx{flex:1}
.hero-t{font-weight:800;font-size:13px;color:var(--mink)}
.hero-s{color:var(--msub);font-size:10.5px}
.minirow{display:flex;gap:8px;padding:7px 14px 3px}
.mini{display:flex;flex-direction:column;align-items:center;gap:3px;font-size:9.5px;color:var(--msub)}
.navbar{display:flex;margin-top:auto;background:var(--glass);border-top:1px solid var(--glassbrd);backdrop-filter:blur(14px);padding:7px 4px 10px}
.nav{flex:1;text-align:center;color:var(--msub);font-size:9.6px;display:flex;flex-direction:column;gap:2px}
.nav i{font-style:normal;font-size:14px}
.nav.on{color:var(--goldtx);font-weight:700}
.nav.on i{border-top:1.5px solid var(--goldtx);padding-top:1px}
.featured{margin:8px 12px 3px;border-radius:6px;padding:11px 13px;position:relative;
 background:color-mix(in srgb, var(--fa) 16%, var(--glass));border:1px solid color-mix(in srgb, var(--fa) 45%, transparent);backdrop-filter:blur(13px)}
.feat-tag{font-size:9.5px;color:var(--goldtx);font-weight:700;margin-bottom:6px}
.feat-row{display:flex;gap:10px;align-items:flex-start}
.feat-n{font-weight:800;font-size:13.5px;color:var(--mink)}
.feat-s{color:var(--mink);opacity:.85;font-size:10.6px;line-height:1.65;margin-top:2px}
.dots{position:absolute;inset-inline-start:13px;top:12px;display:flex;gap:3px;align-items:center}
.dots b{width:12px;height:3px;border-radius:2px;background:var(--goldtx)}
.dots i{width:3px;height:3px;border-radius:50%;background:var(--glassbrd)}
.dim{position:absolute;inset:0;background:#00000055;z-index:2}
body.mock-light .dim{background:#3a2f1f33}
.sheet{position:absolute;bottom:0;left:0;right:0;z-index:3;border-radius:10px 10px 0 0;padding:11px 15px 16px;
 background:color-mix(in srgb, var(--mbg) 76%, transparent);backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);border-top:1px solid var(--glassbrd)}
.grab{width:32px;height:4px;border-radius:2px;background:var(--glassbrd);margin:0 auto 11px}
.dpane{display:flex;gap:11px;align-items:center;border-radius:6px;padding:10px;
 background:color-mix(in srgb, var(--fa) 15%, transparent);border:1px solid color-mix(in srgb, var(--fa) 40%, transparent)}
.dname{font-weight:800;font-size:14.5px;color:var(--mink)}
.dchips{display:flex;gap:5px;margin-top:5px}
.dchips span{background:var(--glass);border:1px solid var(--glassbrd);border-radius:4px;padding:2px 8px;font-size:9.5px;color:var(--msub)}
.dsum{color:var(--msub);font-size:11px;margin:10px 1px}
.feats{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:12px}
.feats span{border:1px solid var(--glassbrd);background:var(--glass);border-radius:5px;padding:3px 10px;font-size:9.8px;color:var(--mink)}
.acq{display:block;text-align:center;border-radius:6px;padding:9px;font-weight:800;font-size:12.5px;margin-top:7px;color:var(--mink);
 background:color-mix(in srgb, var(--fa) 26%, transparent);border:1px solid color-mix(in srgb, var(--fa) 60%, transparent)}
.acq.ghost{background:transparent;border:1px solid var(--glassbrd);color:var(--msub);font-weight:700}
.door .dico{width:38px;height:38px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;
 background:color-mix(in srgb, var(--fa) 18%, transparent);border:1px solid color-mix(in srgb, var(--fa) 40%, transparent);color:var(--mink)}
.door .chev{color:var(--msub)}
@media (max-width:720px){.phone{width:262px;height:526px}}
</style></head><body>
<div class="wrap">
<header class="top">
  <div>
    <h1>مقترح واجهات متجر أمان — <b>«الزجاج المعشّق»</b></h1>
    <div class="sub">النسخة ٣ · اتجاهٌ واحد ملتزم كما وجّهت: زجاجٌ معشّق بوحي وردة أمان لابز · زوايا شبه حادة · لا ذهب مطموساً · 2026-09-03</div>
  </div>
  <button class="toggle" onclick="document.body.classList.toggle('mock-light');this.textContent=document.body.classList.contains('mock-light')?'🌙 عرض النماذج ليلاً':'☀ عرض النماذج نهاراً'">☀ عرض النماذج نهاراً</button>
</header>

<section>
  <h2>قراراتك المثبّتة — كلها نافذة في هذا المقترح</h2>
  <div class="contract new">
    <span>«التحديثات أولاً» معتمدة — بطلُ الرئيسية</span>
    <span>«عضو الأسبوع» معتمدة — قمرية مستثناة من الدوران</span>
    <span>سِتر يخاطب المحجبات بخطابٍ مؤنث</span>
    <span>لا أزرار مطموسة بالأصفر — الذهب خطٌّ شعري ونص، لا ملء</span>
    <span>لغة «فحص التوقيع» أُلغيت نهائياً من كل ما يراه المستخدم</span>
    <span>الزوايا شبه حادة</span>
    <span>تلغرام آخر أبواب الدعم — نُفِّذ في 1.24.26</span>
    <span>خلفيات الأيقونات مقدّسة — هي اللوغو</span>
    <span>ارتفاع الصف لا يزيد بكسلاً</span>
    <span>الليل باردٌ أزرق الميل</span>
  </div>
  <div class="subh">ومن الميثاق القديم: ترتيب الاحتياج اليومي · بنر «فكرة» v5 · الوردة المائية · accentInk · التبويبات الأربعة.</div>
</section>

<section>
  <h2>الفكرة — الضوء عبر النافذة</h2>
  <div class="tagline">
    وردةُ أمان لابز نافذةٌ معشّقة: ثماني بتلاتٍ من سماوات العائلة يفصلها رصاص الليل.
    هذا المقترح يجعل المتجر كله امتداداً لتلك النافذة: أرضيةٌ ليلية باردة تسبح فيها
    <b>بقعُ ضوءٍ</b> بألوان العائلة، وفوقها <b>بطاقاتُ زجاجٍ مصنفر</b> شبه حادة الزوايا
    يرشح الضوء من خلفها، و<b>قوسٌ معشّق</b> من السماوات الخمس يعلو كل صفحة مكان الخيط الشعري.
    الذهب لا يُسكب: خطٌّ شعري حول زرّ التحديث، ونصٌّ لامع للأرقام البطلة، وتوهجٌ خافت حول الوردة.
    كل عضوٍ يحضر بلوحِ زجاجٍ بصبغته هو — لا بطلاءٍ مصمت.
  </div>
  <div class="phones">{{PH1}}{{PH2}}{{PH3}}{{PH4}}</div>
</section>

<section>
  <h2>ما يتغيّر — وما لا يتغيّر</h2>
  <div class="cols">
    <div class="notes">
      <h3>يتغيّر</h3>
      <ul>
        <li>لغة الأسطح كلها: بطاقات زجاجٍ مصنفر (شفافية + ضبابية) بحدودٍ ضوئية رقيقة، بزوايا 6dp شبه حادة — على أرضيةٍ ليلية باردة تشع منها بقع ألوان العائلة.</li>
        <li>الخيط الشعري يترقّى إلى «قوسٍ معشّق»: قطع زجاج السماوات الخمس يفصلها رصاصٌ داكن.</li>
        <li>بطل «التحديثات أولاً»: لوح زجاجٍ برقمٍ ذهبيّ النص وزر «حدّث الكل» بخطٍّ ذهبي شعري — لا ملء.</li>
        <li>«عضو الأسبوع»: لوحُ زجاجٍ بصبغة العضو يتبدل أسبوعياً محلياً — قمرية خارج الدوران، وسِتر بخطابه المؤنث الجديد.</li>
        <li>أزرار الأفعال كلها زجاجية: «تحديث» بخط ذهبي، «تنزيل/فتح» بحدٍّ زجاجي محايد، وزر الاقتناء في التفاصيل زجاجُ صبغةِ العضو.</li>
        <li>وردة المتجر في الترويسة بتوهجٍ خافت — الضوء عبر النافذة.</li>
      </ul>
      <h3>لا يتغيّر</h3>
      <ul>
        <li>ارتفاع الصف وبلاطة 40dp والبنية الثلاثية — حرفياً كما اليوم.</li>
        <li>أيقونات الأعضاء بسمائها الكاملة — تزداد إشراقاً فوق الزجاج لا غير.</li>
        <li>ترتيب القائمة، بنر «فكرة» v5، الوردة المائية، التبويبات الأربعة.</li>
      </ul>
      <h3>صدقُ التنفيذ</h3>
      <ul>
        <li>الضبابية الحقيقية (blur) متاحة من أندرويد 12 فصاعداً؛ وما دونه يأخذ زجاجاً شفيفاً بلا ضبابية — نفس الروح، متدرجة بأمانة.</li>
        <li>حبّة البحث وبطل التحديثات يُبنيان مع هذا الثوب في إصدارٍ واحد.</li>
      </ul>
      <div class="meta"><span class="m-imp">الأثر: هويةٌ لا تشبه أحداً — نافذة أمان</span><span class="m-cost">الكلفة: متوسطة-عالية (Theme جديد + Screens، بلا منطق خطر)</span><span class="m-risk">الخطر: أداء الضبابية على الأجهزة الضعيفة — مسوّى بالتدرج أعلاه</span></div>
    </div>
  </div>
  <div class="reco">
    <b>إن أعجبك الثوب:</b> كلمة «نفّذ الزجاج» تطلق 1.25.0 = الزجاج المعشّق + التحديثات أولاً + عضو الأسبوع (بقواعده) دفعةً واحدة.
    وأي تفصيلةٍ هنا قابلة للتبديل قبلها — <b>لا يُنفَّذ حرف قبل قرارك</b>.
  </div>
</section>

<footer>من مختبرات أمان · ورقة داخلية للمالك — لا تُنشر · النماذج تقريبية والتنفيذ النهائي أدقّ منها</footer>
</div>
<script>if(location.hash==='#light'){document.body.classList.add('mock-light');document.querySelector('.toggle').textContent='🌙 عرض النماذج ليلاً'}</script>
</body></html>
"""

def main():
    html = (HTML.replace("{{PH1}}", mock_home_updates())
                .replace("{{PH2}}", mock_home_featured())
                .replace("{{PH3}}", mock_detail())
                .replace("{{PH4}}", mock_support()))
    io.open(OUT, "w", encoding="utf-8").write(html)
    print("written:", OUT, len(html), "chars")

if __name__ == "__main__":
    main()
