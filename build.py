#!/usr/bin/env python3
"""Build the site from src/.

src/template.html  -> index.html          (sales page: Spin, Grabb, Gist, ReelScroll and WhatsTime)
src/company.html   -> company/index.html  (Spoon Software home)
src/privacy.html   -> privacy/index.html  (Privacy Policy)

Embeds the app icons, adds the shared head and footer, and fills in the contact address.
"""
import base64
import pathlib
import re

CONTACT = "support@spoon.com.br"  # support address shown on the site
BUNDLE_URL = "https://buy.stripe.com/6oUaEW5W45u6bIp5I73AY03"  # Stripe Payment Link for Spin and Grabb together

root = pathlib.Path(__file__).resolve().parent
src = root / "src"


def data_uri(name):
    return "data:image/png;base64," + base64.b64encode((src / name).read_bytes()).decode()


ICONS = {"{{SPIN}}": data_uri("spin.png"), "{{Grabb}}": data_uri("grabb.png"), "{{GIST}}": data_uri("gist.png"),
         "{{REELSCROLL}}": data_uri("reelscroll.png"), "{{WHATSTIME}}": data_uri("whatstime.png")}


def spoon_logo(size_class=""):
    """Animated Spoon Software logo: the S from design/make_logo.py in neon layers.

    Same layers as the app icons: a wide blurred glow, a soft glow, the coloured line,
    and a thin white core. Each coloured layer is a rotating conic gradient masked by
    the S outline stroked at that layer's width.
    """
    d = (root / "design" / "logo-s.path").read_text().strip()

    def mask(width):
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 824 824">'
               f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{width}" '
               'stroke-linejoin="round" stroke-linecap="round"/></svg>')
        uri = "url('data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode() + "')"
        return f'style="-webkit-mask-image:{uri};mask-image:{uri}"'

    return (
        f'<div class="{("slogo " + size_class).strip()}" role="img" aria-label="Spoon Software logo">'
        f'<div class="g g1"><i {mask(12)}></i></div>'
        f'<div class="g g2"><i {mask(7)}></i></div>'
        f'<div class="g"><i {mask(5)}></i></div>'
        '<svg class="core" viewBox="0 0 824 824" aria-hidden="true">'
        f'<path d="{d}"/></svg></div>'
    )


ICONS["{{SLOGO}}"] = spoon_logo()

# Header on every page: small Spoon Software logo on the left.
HEADER = (src / "header.html").read_text().replace("{{SLOGO_SM}}", spoon_logo("sm"))
# App tiles on the company page and the sales page. Hover shows more, a click goes to the app box.
APP_TILES = (src / "app-tiles.html").read_text()

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{description}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Spoon Software">
<meta property="og:image" content="https://spoon.com.br/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Spoon Software: Spin and Grabb, small Mac apps for simple tasks.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://spoon.com.br/og-image.png">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
"""

FOOTER_ROW = (
    '<div class="row"><span>© 2026 Spoon Software. All rights reserved.</span>'
    '<nav aria-label="Site"><a href="/">Apps</a><a href="/bundle/">Bundle</a><a href="/company/">Spoon Software</a>'
    '<a href="/privacy/">Privacy Policy</a><a href="#" id="cookie-settings">Cookies</a></nav></div>'
)

FOOTER = f"""<footer>
  <div class="wrap">
    {FOOTER_ROW}
  </div>
</footer>
"""

# Styles for the company and privacy pages, on top of the shared base taken from the sales page.
PAGE_CSS = """
.contact{padding-bottom:64px}
.contact p{font-size:19px}

/* privacy page */
.doc{max-width:760px;padding-block:48px 64px}
.doc .crumb{font-size:14px;margin-bottom:28px}
.doc h1{font-size:clamp(40px,6vw,56px);line-height:1.05}
.doc .meta{color:var(--ink-2);font-size:14px;margin:10px 0 28px}
.doc .lead{font-size:21px;line-height:1.4;padding:20px 24px;background:var(--tile);border-radius:18px}
.doc h2{font-size:24px;margin:40px 0 10px}
.doc p+p{margin-top:12px}
.doc ul,.doc ol{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:10px}

/* download pages */
.dl{text-align:left}
.dl-icon{width:128px;height:auto;margin-bottom:20px;filter:drop-shadow(0 14px 22px rgba(0,0,0,.2))}
.dl h1{margin-bottom:20px}
.dl-btn{display:flex;flex-wrap:wrap;align-items:center;gap:12px 16px;margin:32px 0 8px}
.dl-btn .pill{font-size:19px;padding:13px 28px}
.dl-btn span{color:var(--ink-2);font-size:14px}
.dl ol+p{margin-top:16px}
.dl .dl-btn+.dl-btn{margin-top:0}

/* bundle page and the bundle download page */
.pair{display:flex;justify-content:center;gap:clamp(12px,3vw,24px);margin-bottom:28px}
.pair img{width:clamp(96px,14vw,148px);height:auto;filter:drop-shadow(0 18px 28px rgba(0,0,0,.22))}
.pair-left{justify-content:flex-start;margin-bottom:20px}
.pair-left img{width:112px}
.bundle-card{background:var(--tile);border-radius:32px;padding:clamp(28px,5vw,56px);display:flex;flex-direction:column;gap:16px;max-width:760px;margin:0 auto}
.bundle-apps{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:16px}
.bundle-app{display:flex;align-items:center;gap:16px;color:var(--ink)}
.bundle-app:hover{text-decoration:none}
.bundle-app img{width:72px;height:auto;flex:none;filter:drop-shadow(0 10px 16px rgba(0,0,0,.18))}
.bundle-app b{display:block;font-size:24px;font-weight:600;letter-spacing:-.03em}
.bundle-app small{display:block;font-size:15px;color:var(--ink-2)}
.buy{display:flex;flex-wrap:wrap;align-items:center;gap:14px 18px;margin-top:8px;padding-top:20px;border-top:1px solid var(--line)}
.buy .price{font-size:34px;font-weight:600;letter-spacing:-.035em;font-variant-numeric:tabular-nums;line-height:1}
.buy .price small{font-size:14px;font-weight:400;color:var(--ink-2);letter-spacing:0;margin-left:4px}
.buy .price s{font-size:17px;font-weight:400;color:var(--ink-2);letter-spacing:0;margin-left:10px}
.buy .pill{font-size:17px;padding:11px 24px}
.terms{width:100%;display:flex;flex-wrap:wrap;gap:4px 14px;font-size:13px;color:var(--ink-2)}
.terms span::before{content:"\\2713\\00a0";color:var(--ok);font-weight:600}
.req{font-size:13px;color:var(--ink-2)}
.bundle-what{padding-bottom:64px}
.bundle-what .bundle-card{max-width:1000px}
.duo{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:clamp(20px,4vw,40px)}
.duo-app{display:flex;flex-direction:column;gap:14px;min-width:0}
.duo-head{display:flex;align-items:center;gap:16px;color:var(--ink)}
.duo-head:hover{text-decoration:none}
.duo-head img{width:72px;height:auto;flex:none;filter:drop-shadow(0 10px 16px rgba(0,0,0,.18))}
.duo-head b{display:block;font-size:28px;font-weight:600;letter-spacing:-.03em}
.duo-head small{display:block;font-size:15px;color:var(--ink-2)}
.duo-app .demo{position:relative;aspect-ratio:5/4;border-radius:18px;overflow:hidden;background:#111;
  box-shadow:0 24px 48px -24px rgba(0,0,0,.5),0 0 0 1px rgba(0,0,0,.08)}
.duo-app video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.duo-app p{color:var(--ink-2)}
"""


# Free apps: the buttons on the sales page download the zip at once, through the trial counter.
TRIAL_COUNTER = "https://spoon-license.spoonsoftware.workers.dev/trial/"
FREE_ZIPS = {"gist": "Gist-1.0.0.zip", "reelscroll": "ReelScroll-1.0.4.zip", "whatstime": "WhatsTime-1.0.0.zip"}
FREE_DL = {"{{%s_DL}}" % app.upper(): f"{TRIAL_COUNTER}{app}?f={zip_name}" for app, zip_name in FREE_ZIPS.items()}


def fill(html):
    html = html.replace("{{APP_TILES}}", APP_TILES).replace("{{HEADER}}", HEADER)
    for key, value in ICONS.items():
        html = html.replace(key, value)
    html = html.replace("{{BUNDLE_URL}}", BUNDLE_URL)
    for key, value in FREE_DL.items():
        html = html.replace(key, value)
    html = html.replace("{{CONTACT}}", CONTACT).replace("{{FOOTER_ROW}}", FOOTER_ROW)
    leftover = re.findall(r"\{\{[A-Za-z_]+\}\}", html)
    assert not leftover, f"unreplaced placeholders: {leftover}"
    return html


# Meta Pixel and cookie choice, added to every page. The Pixel loads only after the visitor accepts.
PURCHASES = {
    "get/bcdr7W5qZ4ol/index.html": ("Spin", 5),
    "get/XN5POMsYFafm/index.html": ("Grabb", 5),
    "get/sw8jntSb82WU/index.html": ("Spin and Grabb", 8),
}
CONSENT = (src / "consent.html").read_text()
# The phone version of the trial pages, added to every page.
SITE = (src / "site.html").read_text()


def write(rel, html):
    purchase = "null"
    if rel in PURCHASES:
        name, value = PURCHASES[rel]
        purchase = '{content_name:"%s",value:%d,currency:"USD"}' % (name, value)
    if 'class="site-head"' not in html:
        assert "<main" in html, rel
        html = html.replace("<main", HEADER + "<main", 1)
    html = html.rstrip() + "\n" + SITE + CONSENT.replace("{{PURCHASE}}", purchase)
    out = root / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(f"{rel}: {out.stat().st_size} bytes")


template = (src / "template.html").read_text()

# Sales page: the template carries its own styles and footer.
body = template.replace('<meta charset="utf-8">\n', "", 1)
write("index.html", HEAD.format(
    description="Spin cleans up your Desktop in style. Grabb gets videos from anywhere. "
                "Gist keeps only the article of a web page and shortens it, for free. "
                "ReelScroll moves Instagram Reels on when a video ends, for free. "
                "WhatsTime schedules WhatsApp messages, for free. "
                "Small Mac apps for simple tasks.",
    og_title="Spin, Grabb, Gist, ReelScroll and WhatsTime") + fill(body) + "\n")

# Shared base: colour tokens, type, links, layout and hero, plus the footer rules.
style = template[template.index("<style>") + len("<style>"):template.index("</style>")]
base = style[style.index(":root{"):style.index("/* app sections */")]
footer_start = style.index("footer{")
footer_css = style[footer_start:style.index("@media (prefers-reduced-motion", footer_start)]
css = "<style>\n" + base + footer_css + PAGE_CSS + "</style>\n"

pages = {
    "company/index.html": ("company.html",
                           "Spoon Software makes small Mac apps for simple tasks: Spin, Grabb, Gist, ReelScroll and WhatsTime.",
                           "Spoon Software"),
    "bundle/index.html": ("bundle.html",
                          "Spin and Grabb together for 8 dollars, once. Both Mac apps with lifetime upgrades.",
                          "Spin and Grabb Bundle"),
    "privacy/index.html": ("privacy.html",
                           "How Spoon Software handles your data in Spin, Grabb, Gist, ReelScroll, WhatsTime and on this website.",
                           "Privacy Policy · Spoon Software"),
}
for rel, (name, description, og_title) in pages.items():
    page = (src / name).read_text()
    write(rel, HEAD.format(description=description, og_title=og_title) + css + fill(page) + FOOTER)

# Download pages. Stripe Payment Links send buyers here after payment. The addresses are
# random and not linked from the site; the zips are assets of a public GitHub release.
RELEASE = "https://github.com/Neto/spoon.com.br/releases/download/downloads-2026-11/"
DOWNLOADS = {
    "get/bcdr7W5qZ4ol/index.html": ("Spin", "{{SPIN}}", "Spin-1.9.7.zip", "2.6 MB"),
    "get/XN5POMsYFafm/index.html": ("Grabb", "{{Grabb}}", "Grabb-1.10.2.zip", "82 MB"),
}
download = (src / "download.html").read_text()
for rel, (app, icon, zip_name, size) in DOWNLOADS.items():
    page = (download.replace("{{APP}}", app).replace("{{ICON}}", icon)
            .replace("{{ZIP_URL}}", RELEASE + zip_name).replace("{{ZIP_NAME}}", zip_name)
            .replace("{{SIZE}}", size))
    write(rel, HEAD.format(description=f"Download {app}.", og_title=f"Download {app}")
          + css + fill(page) + FOOTER)

# Public trial download pages (linked from the site and from the license server).
# The button goes through the license Worker, which counts trial downloads per app per day
# (totals only) and sends the visitor on to the zip.
trial = (src / "trial.html").read_text()
for app, icon in (("Spin", "{{SPIN}}"), ("Grabb", "{{Grabb}}")):
    zip_name, size = next((z, s) for a, _, z, s in DOWNLOADS.values() if a == app)
    page = (trial.replace("{{APP}}", app).replace("{{ICON}}", icon)
            .replace("{{TRIAL_URL}}", f"{TRIAL_COUNTER}{app.lower()}?f={zip_name}")
            .replace("{{ZIP_NAME}}", zip_name).replace("{{SIZE}}", size))
    write(f"download/{app.lower()}/index.html", HEAD.format(description=f"Download {app} for Mac. Free 7 day trial.", og_title=f"Download {app}")
          + css + fill(page) + FOOTER)

# Gist is free: its download page also goes through the trial counter, as "gist".
FREE_ZIP, FREE_SIZE = FREE_ZIPS["gist"], "1.3 MB"
page = ((src / "free.html").read_text().replace("{{APP}}", "Gist").replace("{{ICON}}", "{{GIST}}")
        .replace("{{TRIAL_URL}}", f"{TRIAL_COUNTER}gist?f={FREE_ZIP}")
        .replace("{{ZIP_NAME}}", FREE_ZIP).replace("{{SIZE}}", FREE_SIZE))
write("download/gist/index.html", HEAD.format(description="Download Gist for Mac, free.", og_title="Download Gist")
      + css + fill(page) + FOOTER)

# ReelScroll is free too: its download page also goes through the trial counter, as "reelscroll".
REEL_ZIP, REEL_SIZE = FREE_ZIPS["reelscroll"], "0.8 MB"
page = ((src / "free-reelscroll.html").read_text().replace("{{APP}}", "ReelScroll").replace("{{ICON}}", "{{REELSCROLL}}")
        .replace("{{TRIAL_URL}}", f"{TRIAL_COUNTER}reelscroll?f={REEL_ZIP}")
        .replace("{{ZIP_NAME}}", REEL_ZIP).replace("{{SIZE}}", REEL_SIZE))
write("download/reelscroll/index.html", HEAD.format(description="Download ReelScroll for Mac, free.", og_title="Download ReelScroll")
      + css + fill(page) + FOOTER)

# WhatsTime is free too: its download page also goes through the trial counter, as "whatstime".
WT_ZIP, WT_SIZE = FREE_ZIPS["whatstime"], "1.5 MB"
page = ((src / "free-whatstime.html").read_text().replace("{{APP}}", "WhatsTime").replace("{{ICON}}", "{{WHATSTIME}}")
        .replace("{{TRIAL_URL}}", f"{TRIAL_COUNTER}whatstime?f={WT_ZIP}")
        .replace("{{ZIP_NAME}}", WT_ZIP).replace("{{SIZE}}", WT_SIZE))
write("download/whatstime/index.html", HEAD.format(description="Download WhatsTime for Mac, free.", og_title="Download WhatsTime")
      + css + fill(page) + FOOTER)

# Bundle download page: one payment, both installers.
BUNDLE_PAGE = "get/sw8jntSb82WU/index.html"
page = (src / "download-bundle.html").read_text()
for app, key in (("Spin", "SPIN"), ("Grabb", "GRABB")):
    zip_name, size = next((z, s) for a, _, z, s in DOWNLOADS.values() if a == app)
    page = (page.replace("{{%s_ZIP_URL}}" % key, RELEASE + zip_name)
            .replace("{{%s_ZIP_NAME}}" % key, zip_name).replace("{{%s_SIZE}}" % key, size))
write(BUNDLE_PAGE, HEAD.format(description="Download Spin and Grabb.", og_title="Download Spin and Grabb")
      + css + fill(page) + FOOTER)
