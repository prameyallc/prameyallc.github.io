#!/usr/bin/env python3
"""Generate the Prameya LLC company site.

Sources live in src/. Generated HTML at the repo root is what GitHub Pages
serves. Do not hand-edit the generated files.

    python3 src/build_site.py
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SRC = Path(__file__).resolve().parent
BASE_URL = "https://prameyallc.github.io"
PRIVACY_HUB = f"{BASE_URL}/privacy/"
SUPPORT_URL = f"{BASE_URL}/privacy/support/"
EMAIL = "admin@prameya.legal"
X_URL = "https://x.com/PrameyaLLC"
GITHUB_URL = "https://github.com/prameyallc"
HF_APPS = {"omnisalub", "omnident", "omnilex"}

NAV = [
    ("apps/", "Apps"),
    ("pricing/", "Pricing"),
    ("standard/", "Standard"),
    ("about/", "About"),
    ("privacy-model/", "Privacy"),
    ("contact/", "Contact"),
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def prefix(depth: int) -> str:
    return "" if depth == 0 else "../" * depth


def href(depth: int, dest: str) -> str:
    p = prefix(depth)
    if dest == "":
        return "./" if depth == 0 else p
    return f"{p}{dest}"


def load_catalog() -> dict:
    return json.loads((SRC / "apps.json").read_text(encoding="utf-8"))


def apps_by_slug(catalog: dict) -> dict:
    return {app["slug"]: app for app in catalog["apps"]}


def group_for(catalog: dict, group_id: str) -> dict:
    for group in catalog["groups"]:
        if group["id"] == group_id:
            return group
    raise KeyError(group_id)


def status_label(app: dict) -> str:
    if app.get("store_url") and app.get("status") == "available":
        return "On the App Store"
    return "In development"


def status_class(app: dict) -> str:
    if app.get("store_url") and app.get("status") == "available":
        return "status available"
    return "status"


def mailto(subject: str) -> str:
    return f"mailto:{EMAIL}?subject={quote(subject)}"


def jsonld_organization() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Prameya LLC",
        "url": f"{BASE_URL}/",
        "email": EMAIL,
        "sameAs": [GITHUB_URL, X_URL],
    }


def jsonld_home(catalog: dict) -> dict:
    elements = []
    for i, app in enumerate(catalog["apps"], start=1):
        elements.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": app["name"],
                "url": f"{BASE_URL}/apps/{app['slug']}/",
            }
        )
    return {
        "@context": "https://schema.org",
        "@graph": [
            jsonld_organization(),
            {
                "@type": "ItemList",
                "name": "Prameya apps",
                "numberOfItems": len(catalog["apps"]),
                "itemListElement": elements,
            },
        ],
    }


def jsonld_app(app: dict) -> dict:
    node = {
        "@type": "SoftwareApplication",
        "name": app["legal_name"],
        "url": f"{BASE_URL}/apps/{app['slug']}/",
        "creator": jsonld_organization(),
        "description": app["meta_description"],
        "creativeWorkStatus": "Incomplete",
    }
    return {"@context": "https://schema.org", "@graph": [jsonld_organization(), node]}


def render_nav(depth: int, current: str) -> str:
    def items() -> str:
        out = []
        for dest, label in NAV:
            key = dest.rstrip("/")
            current_attr = ' aria-current="page"' if current == key else ""
            out.append(f'<a href="{href(depth, dest)}"{current_attr}>{esc(label)}</a>')
        return "".join(out)

    home_current = ' aria-current="page"' if current == "home" else ""
    links = items()
    return f"""<nav class="site" aria-label="Primary"><div class="wrap">
  <a class="brand" href="{href(depth, '')}"{home_current}>Prameya<span>.</span></a>
  <div class="navlinks nav-desktop">{links}</div>
  <details class="nav-mobile">
    <summary>Menu</summary>
    <div class="navlinks">{links}</div>
  </details>
</div></nav>"""


def render_footer(depth: int) -> str:
    return f"""<footer class="site"><div class="wrap">
  <div>© 2026 Prameya LLC</div>
  <nav aria-label="Footer">
    <a href="{GITHUB_URL}">GitHub</a>
    <a href="{X_URL}">X @PrameyaLLC</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <a href="{href(depth, 'privacy-model/')}">Privacy</a>
    <a href="{PRIVACY_HUB}">App policies</a>
    <a href="{href(depth, 'resources/')}">Resources</a>
    <a href="{href(depth, 'contact/')}">Contact</a>
  </nav>
</div>
<div class="wrap"><p class="fine">All eleven apps are in active development and are not yet available on the App Store.
Nothing on this site is medical, legal, financial or engineering advice. None of these apps
represents you in a legal matter or recommends an investment. None of them is a substitute
for a licensed professional.</p></div>
</footer>"""


def chips(items: list[str]) -> str:
    if not items:
        return ""
    return '<ul class="chips">' + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def format_price(price: float) -> str:
    """Format price with 2 decimal places or as integer if whole number."""
    if price == int(price):
        return f"${int(price)}"
    return f"${price:.2f}"


def pricing_table(app: dict) -> str:
    """Generate pricing tier table HTML for an app."""
    if "pricing" not in app:
        return ""

    pricing = app["pricing"]
    free = pricing.get("free_tier", {})
    pro = pricing.get("pro_subscription", {})

    free_features = "".join(f"<li>{esc(f)}</li>" for f in free.get("includes", []))
    pro_features = "".join(f"<li>{esc(f)}</li>" for f in pro.get("includes", []))

    pro_monthly = format_price(pro.get("price_monthly_usd", 0))
    pro_yearly = format_price(pro.get("price_yearly_usd", 0))
    pro_life = format_price(pro.get("price_lifetime_usd", 0))

    return f"""<div class="pricing-tiers">
  <div class="kicker">Pricing</div>
  <h2>Free knowledge. Optional Pro tools.</h2>
  <div class="tier-grid">
    <div class="tier">
      <h3>Free</h3>
      <div class="tier-price">$0</div>
      <ul class="tier-features">{free_features}</ul>
    </div>
    <div class="tier featured">
      <h3>Pro</h3>
      <div class="tier-price">{pro_monthly}/mo</div>
      <div class="tier-note">{pro_yearly}/year · {pro_life} lifetime</div>
      <ul class="tier-features">{pro_features}</ul>
    </div>
  </div>
  <p class="pricing-note">The reference library stays free. Pro is monthly, annual, or lifetime — the same tools either way. 7-day trial on monthly and annual. Family Sharing on. Cancel in Settings.</p>
</div>"""


def app_card(app: dict, depth: int, *, compact: bool) -> str:
    p = prefix(depth)
    more = "" if compact else chips(app["features"] + (app.get("platforms") or []))
    blurb = app["summary"] if not compact else app["summary"]
    learn = f'<span class="more">Learn more →</span>'
    return f"""<a class="app" style="--a:{esc(app['accent'])}" href="{href(depth, f"apps/{app['slug']}/")}">
  <span class="{status_class(app)}">{esc(status_label(app))}</span>
  <div class="app-top"><img src="{p}assets/icons/{esc(app['icon'])}" alt="{esc(app['name'])} icon" width="46" height="46">
    <div><div class="app-name">{esc(app['name'])}</div><div class="app-for">{esc(app['audience'])}</div></div></div>
  <p>{esc(blurb)}</p>
  {more}
  {learn}
</a>"""


def groups_grid(catalog: dict, depth: int, *, compact: bool) -> str:
    by_slug = apps_by_slug(catalog)
    blocks = []
    for group in catalog["groups"]:
        cards = "".join(app_card(by_slug[slug], depth, compact=compact) for slug in group["slugs"])
        blocks.append(
            f"""<div class="group">
    <div class="group-head"><h3>{esc(group['name'])}</h3><span>{esc(group['blurb'])}</span></div>
    <div class="apps">{cards}</div>
  </div>"""
        )
    return "\n".join(blocks)


def page(
    *,
    title: str,
    description: str,
    canonical: str,
    depth: int,
    current: str,
    body: str,
    jsonld: dict,
) -> str:
    p = prefix(depth)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{esc(canonical)}">
<meta name="theme-color" content="#0B0B0E">
<link rel="icon" href="{p}assets/icons/OmniSalub.png">
<link rel="stylesheet" href="{p}assets/css/site.css">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{render_nav(depth, current)}
<main id="main">
{body}
</main>
{render_footer(depth)}
</body>
</html>
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def home_body(catalog: dict) -> str:
    return f"""<header class="hero"><div class="wrap">
  <span class="eyebrow">Prameya LLC</span>
  <h1>Expert knowledge, <em>for everyone</em>.</h1>
  <p class="lede">
    A doctor, a lawyer, a financial planner, a structural engineer — each carries knowledge most
    people can only rent by the hour. We build apps that hand you that knowledge directly: in plain
    language, with its sources, running entirely on your own device.
  </p>
  <div class="cta">
    <a class="btn primary" href="{href(0, 'apps/')}">See the portfolio</a>
    <a class="btn ghost" href="{href(0, 'standard/')}">How they're built</a>
    <a class="btn ghost" href="{mailto('Prameya')}">Write to us</a>
  </div>
</div></header>

<section id="how"><div class="wrap">
  <div class="kicker">The standard</div>
  <h2>Four rules every app follows.</h2>
  <p class="sub">Not marketing lines — constraints we build against. They decide what these apps are
    allowed to say to you.</p>
  <div class="principles">
    <div class="p"><h3>Runs on your device</h3>
      <p>No account, no server, no analytics. The models run locally. What you record simply stays
         where you made it. Narrow exceptions — model-file downloads on three apps — are described
         on the <a class="inline" href="{href(0, 'privacy-model/')}">privacy model</a> page.</p></div>
    <div class="p"><h3>Every claim has a source</h3>
      <p>Where an app states something professional, it cites where that came from — and where a
         source is missing, it says so instead of filling the gap.</p></div>
    <div class="p"><h3>The knowledge layer is free</h3>
      <p>"For everyone" would be hollow behind a paywall. Reference, education and safety content stay
         free. Paid tiers buy depth and convenience, never access to knowing.</p></div>
    <div class="p"><h3>It won't pretend to be your professional</h3>
      <p>These apps prepare you, organise you and explain things. They don't diagnose you, represent
         you or advise you. That line is drawn in the code, not the small print.</p></div>
  </div>
</div></section>

<section id="apps"><div class="wrap">
  <div class="kicker">The portfolio</div>
  <h2>Ten apps. One idea.</h2>
  <p class="sub">Each takes a field where expertise is expensive and asks the same question: what does
    the professional actually know — and how much of it can you simply be handed?</p>
  {groups_grid(catalog, 0, compact=True)}
</div></section>

<section id="vision" class="vision"><div class="wrap">
  <div class="kicker">Why</div>
  <blockquote>Expertise shouldn't be something you can only rent.</blockquote>
  <div class="cols">
    <div>
      <p>Most professional knowledge isn't secret. It is <strong>public, written down, and largely
      unreadable</strong> — scattered across codes and guidelines, in a register written for
      colleagues rather than for the people it describes.</p>
      <p style="margin-top:var(--sp-m)">What you actually pay a professional for is usually two things: the translation, and the
      judgement. The judgement is real and worth paying for. <strong>The translation shouldn't cost
      an hourly rate.</strong></p>
    </div>
    <div>
      <p>So each app takes one field and does the translation — carefully, with sources, and with a
      hard line at the point where genuine professional judgement begins.</p>
      <p style="margin-top:var(--sp-m)">The result is meant to make you a <strong>better client, not a substitute for one</strong>:
      someone who walks in prepared, asks sharper questions, and knows which parts they can handle
      themselves.</p>
    </div>
  </div>
  <p class="note">All eleven apps are in active development and are not yet available on the App Store.
    Nothing on this page is medical, legal, financial or engineering advice. None of these apps
    represents you in a legal matter or recommends an investment. None of them is a substitute
    for a licensed professional.</p>
</div></section>"""


def apps_index_body(catalog: dict) -> str:
    return f"""<header class="page-hero"><div class="wrap">
  <div class="kicker">The portfolio</div>
  <h1>Eleven apps. One idea.</h1>
  <p class="lede">Each takes a field where expertise is expensive and asks the same question: what does
    the professional actually know — and how much of it can you simply be handed?</p>
</div></header>
<section><div class="wrap">
  {groups_grid(catalog, 1, compact=False)}
</div></section>"""


def app_page_body(app: dict, catalog: dict, depth: int) -> str:
    p = prefix(depth)
    group = group_for(catalog, app["group"])
    by_slug = apps_by_slug(catalog)
    related = [by_slug[s] for s in group["slugs"] if s != app["slug"]]
    related_html = "".join(app_card(other, depth, compact=True) for other in related)

    store = ""
    if app.get("store_url"):
        store = f'<a class="btn primary" href="{esc(app["store_url"])}">View on the App Store</a>'

    platforms = chips(app.get("platforms") or [])
    features = chips(app["features"])
    legal = ""
    if app["name"] != app["legal_name"]:
        legal = f'<p class="sub">Published as {esc(app["legal_name"])}.</p>'

    health = ""
    if app.get("health_data_url"):
        health = (
            f'<a class="btn ghost" href="{esc(app["health_data_url"])}">Consumer health data policy</a>'
        )

    hf = ""
    if app["slug"] in HF_APPS:
        hf = f"""<p>This app can download AI model weights from Hugging Face when you tap to install
        them in Settings. That request is for a model file; it does not send your content anywhere.
        The <a class="inline" href="{esc(app['privacy_url'])}">privacy policy</a> is the source for that sentence.</p>"""

    return f"""<header class="page-hero"><div class="wrap" style="--a:{esc(app['accent'])}">
  <span class="{status_class(app)}">{esc(status_label(app))}</span>
  <div class="app-hero-row">
    <img src="{p}assets/icons/{esc(app['icon'])}" alt="{esc(app['name'])} icon" width="72" height="72">
    <div>
      <h1>{esc(app['name'])}</h1>
      <div class="app-for">{esc(app['audience'])}</div>
    </div>
  </div>
  {legal}
  <p class="lede">{esc(app['summary'])}</p>
  <div class="cta">
    <a class="btn primary" href="{mailto(app['name'])}">Write to us about {esc(app['name'])}</a>
    {store}
    <a class="btn ghost" href="{esc(app['privacy_url'])}">Privacy policy</a>
    {health}
  </div>
</div></header>

<section><div class="wrap prose">
  <p>{esc(app['detail'])}</p>
  {features}
  {platforms}
  <div class="hard-line" style="--a:{esc(app['accent'])}">
    <div class="kicker">The line it does not cross</div>
    <p>{esc(app['hard_line'])}</p>
  </div>
  {hf}
  {pricing_table(app)}
  <figure class="shot" style="--a:{esc(app['accent'])}">
    <img src="{p}assets/icons/{esc(app['icon'])}" alt="">
    <figcaption>Screenshots will appear here when a public build is ready.</figcaption>
  </figure>
  <p>Availability is posted on this page when an App Store link exists. Writing to us does not
  add you to a mailing list — that inbox is read by a person.</p>
</div></section>

<section><div class="wrap">
  <div class="kicker">Also in {esc(group['name'])}</div>
  <h2>Related apps</h2>
  <div class="apps" style="margin-top:var(--sp-l)">{related_html}</div>
</div></section>"""


def app_mailto_list(catalog: dict) -> str:
    items = []
    for app in catalog["apps"]:
        items.append(
            f'<li><a class="btn ghost" href="{mailto(app["name"])}">Write about {esc(app["name"])}</a></li>'
        )
    return '<ul class="links-row" style="list-style:none;padding:0">' + "".join(items) + "</ul>"


def brand_swatches(catalog: dict) -> str:
    cells = []
    for app in catalog["apps"]:
        cells.append(
            f"""<figure class="swatch"><div class="chip" style="background:{esc(app['accent'])}"></div>
            <figcaption>{esc(app['name'])}<br><code>{esc(app['accent'])}</code></figcaption></figure>"""
        )
    return '<div class="swatches">' + "".join(cells) + "</div>"


def icon_grid(catalog: dict, depth: int) -> str:
    p = prefix(depth)
    cells = []
    for app in catalog["apps"]:
        cells.append(
            f"""<figure><img src="{p}assets/icons/{esc(app['icon'])}" alt="{esc(app['name'])} icon" width="64" height="64">
            <figcaption>{esc(app['name'])}</figcaption></figure>"""
        )
    return '<div class="icon-grid">' + "".join(cells) + "</div>"


def portfolio_rows(catalog: dict) -> str:
    rows = []
    for app in catalog["apps"]:
        rows.append(
            f"<tr><th>{esc(app['name'])}</th><td>{esc(app['audience'])}</td>"
            f"<td>{esc(app['hard_line'])}</td></tr>"
        )
    return (
        '<div class="tablewrap"><table><thead><tr><th>App</th><th>For</th>'
        "<th>The line it does not cross</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
    )


def load_fragment(name: str, depth: int, catalog: dict) -> str:
    text = (SRC / "pages" / name).read_text(encoding="utf-8")
    return (
        text.replace("{{prefix}}", prefix(depth))
        .replace("{{home}}", href(depth, ""))
        .replace("{{apps}}", href(depth, "apps/"))
        .replace("{{pricing}}", href(depth, "pricing/"))
        .replace("{{standard}}", href(depth, "standard/"))
        .replace("{{about}}", href(depth, "about/"))
        .replace("{{privacy}}", href(depth, "privacy-model/"))
        .replace("{{contact}}", href(depth, "contact/"))
        .replace("{{resources}}", href(depth, "resources/"))
        .replace("{{brand}}", href(depth, "resources/brand/"))
        .replace("{{faq}}", href(depth, "resources/faq/"))
        .replace("{{one_company}}", href(depth, "resources/one-pagers/company/"))
        .replace("{{one_portfolio}}", href(depth, "resources/one-pagers/portfolio/"))
        .replace("{{privacy_hub}}", PRIVACY_HUB)
        .replace("{{support}}", SUPPORT_URL)
        .replace("{{email}}", EMAIL)
        .replace("{{mailto}}", mailto("Prameya"))
        .replace("{{github}}", GITHUB_URL)
        .replace("{{x}}", X_URL)
        .replace("{{app_mailtos}}", app_mailto_list(catalog))
        .replace("{{swatches}}", brand_swatches(catalog))
        .replace("{{icons}}", icon_grid(catalog, depth))
        .replace("{{portfolio_rows}}", portfolio_rows(catalog))
    )


def sitemap_xml(urls: list[str]) -> str:
    items = "\n".join(f"  <url><loc>{esc(u)}</loc></url>" for u in urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
"""


def build() -> None:
    catalog = load_catalog()
    urls: list[str] = []

    def emit(rel_path: str, title: str, description: str, canonical_path: str, depth: int, current: str, body: str, ld: dict) -> None:
        canonical = f"{BASE_URL}{canonical_path}"
        write(ROOT / rel_path, page(
            title=title,
            description=description,
            canonical=canonical,
            depth=depth,
            current=current,
            body=body,
            jsonld=ld,
        ))
        urls.append(canonical)

    emit(
        "index.html",
        "Prameya — Expert knowledge for everyone",
        "A portfolio of on-device apps that put professional-grade knowledge — clinical, legal, financial, technical — into ordinary hands. No accounts. No servers. Sources you can check.",
        "/",
        0,
        "home",
        home_body(catalog),
        jsonld_home(catalog),
    )
    emit(
        "apps/index.html",
        "Apps — Prameya",
        "Ten on-device knowledge apps from Prameya LLC. All currently in development.",
        "/apps/",
        1,
        "apps",
        apps_index_body(catalog),
        jsonld_organization(),
    )
    for app in catalog["apps"]:
        emit(
            f"apps/{app['slug']}/index.html",
            f"{app['name']} — Prameya",
            app["meta_description"],
            f"/apps/{app['slug']}/",
            2,
            "apps",
            app_page_body(app, catalog, 2),
            jsonld_app(app),
        )

    static = [
        ("pricing/index.html", 1, "pricing", "Pricing — Prameya",
         "Three ways to access expert knowledge: free reference library, one-time app purchase, or optional Pro subscription. The knowledge layer stays free.",
         "/pricing/", "pricing.html"),
        ("standard/index.html", 1, "standard", "The standard — Prameya",
         "Four rules every Prameya app follows: on-device, sourced, a free knowledge layer, and a hard line at professional judgement.",
         "/standard/", "standard.html"),
        ("about/index.html", 1, "about", "About — Prameya LLC",
         "Prameya LLC is a US company that translates professional knowledge into language you can use, with sources, on your own device.",
         "/about/", "about.html"),
        ("privacy-model/index.html", 1, "privacy-model", "Privacy model — Prameya",
         "How Prameya apps handle data: on-device processing, no Prameya user database, and links to each app's published privacy policy.",
         "/privacy-model/", "privacy-model.html"),
        ("contact/index.html", 1, "contact", "Contact — Prameya LLC",
         "Write to Prameya LLC at admin@prameya.legal. A person reads that inbox. We do not keep a mailing list.",
         "/contact/", "contact.html"),
        ("resources/index.html", 1, "resources", "Resources — Prameya",
         "Brand tokens, copy rules, FAQ and one-pagers for Prameya LLC.",
         "/resources/", "resources.html"),
        ("resources/brand/index.html", 2, "resources", "Brand — Prameya",
         "OHBrand accents, type, components and copy rules for the Prameya company site.",
         "/resources/brand/", "brand.html"),
        ("resources/faq/index.html", 2, "resources", "FAQ — Prameya",
         "On-device processing, sources, the free knowledge layer, availability, privacy and how to write to us.",
         "/resources/faq/", "faq.html"),
        ("resources/one-pagers/company/index.html", 3, "resources", "Company one-pager — Prameya",
         "A one-page summary of Prameya LLC: mission, four rules, contact.",
         "/resources/one-pagers/company/", "one-pager-company.html"),
        ("resources/one-pagers/portfolio/index.html", 3, "resources", "Portfolio one-pager — Prameya",
         "A one-page summary of the ten Prameya apps currently in development.",
         "/resources/one-pagers/portfolio/", "one-pager-portfolio.html"),
    ]
    for rel_path, depth, current, title, description, canon, fragment in static:
        emit(rel_path, title, description, canon, depth, current, load_fragment(fragment, depth, catalog), jsonld_organization())

    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    write(ROOT / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
    write(ROOT / "sitemap.xml", sitemap_xml(urls))
    print(f"Built {len(urls)} pages → {ROOT}")


if __name__ == "__main__":
    try:
        build()
    except Exception as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        raise
