#!/usr/bin/env python3
"""Build static site for GitHub Pages from content/ and templates."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
BUILD = ROOT / "site"
PUBLIC = ROOT / "public"

NAV = [
    ("Selected works", "/work/"),
    ("Klarna - Live Shopping", "/klarna-live-shopping/"),
    ("Klarna - Desktop Store App", "/klarna-desktop-store-app/"),
    ("Tiki - Rewards Program", "/tiki-rewards-program/"),
    ("Tiki - Gamify users journey", "/gamify-users-journey-on-tiki/"),
    ("Aeho - Product Information Management (PIM)", "/aeho-product-information-management-solution/"),
]

SLUGS = {
    "home": "/",
    "work": "/work/",
    "klarna-live-shopping": "/klarna-live-shopping/",
    "klarna-desktop-store-app": "/klarna-desktop-store-app/",
    "tiki-rewards-program": "/tiki-rewards-program/",
    "gamify-users-journey-on-tiki": "/gamify-users-journey-on-tiki/",
    "aeho-product-information-management-solution": "/aeho-product-information-management-solution/",
}

LOGO = "/images/9f8812f1-30f1-489e-b5e8-129e7b6a1ba1.png"
FAVICON = "/images/50f23401-291a-41b2-9212-2a3412ec5a14.png"

SOCIAL_SVG = {
    "linkedin": """<svg viewBox="0 0 30 24" class="icon" aria-hidden="true"><path d="M19.6,19v-5.8c0-1.4-0.5-2.4-1.7-2.4c-1,0-1.5,0.7-1.8,1.3C16,12.3,16,12.6,16,13v6h-3.4c0,0,0.1-9.8,0-10.8H16v1.5h0v0C16.4,9,17.2,7.9,19,7.9c2.3,0,4,1.5,4,4.9V19H19.6z M8.9,6.7C7.7,6.7,7,5.9,7,4.9C7,3.8,7.8,3,8.9,3s1.9,0.8,1.9,1.9C10.9,5.9,10.1,6.7,8.9,6.7z M10.6,19H7.2V8.2h3.4V19z"/></svg>""",
    "email": """<svg viewBox="0 0 30 24" class="icon" aria-hidden="true"><path d="M15,13L7.1,7.1c0-0.5,0.4-1,1-1h13.8c0.5,0,1,0.4,1,1L15,13z M15,14.8l7.9-5.9v8.1c0,0.5-0.4,1-1,1H8.1c-0.5,0-1-0.4-1-1V8.8L15,14.8z"/></svg>""",
}


def nav_html(active_href: str) -> str:
    items = []
    for label, href in NAV:
        cls = ' class="active"' if href == active_href else ""
        li_cls = "gallery-title" if label == "Selected works" else "project-title"
        items.append(f'<li class="{li_cls}"><a href="{href}"{cls}>{label}</a></li>')
    return "\n".join(items)


def shell(title: str, active_href: str, main_body: str) -> str:
    nav = nav_html(active_href)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="Senior Product Designer" />
  <meta name="robots" content="noindex" />
  <title>{title}</title>
  <link rel="icon" href="{FAVICON}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/main.css" />
  <link rel="stylesheet" href="/css/theme.css" />
  <link rel="stylesheet" href="/css/site.css" />
  <script src="/js/auth.js" defer></script>
  <script src="/js/site.js" defer></script>
</head>
<body class="link-transition">
  <div class="js-responsive-nav">
    <div class="responsive-nav has-social">
      <div class="close-responsive-click-area js-close-responsive-nav">
        <div class="close-responsive-button"></div>
      </div>
      <nav>
        <ul class="group">{nav}</ul>
        <div class="link-title">
          <a href="https://drive.google.com/file/d/1loWXdPouvD5Cz0y9K4oYEMI8gLpN_6Ct/view?usp=sharing" target="_blank" rel="noopener">Resume</a>
        </div>
        <div class="social pf-nav-social">
          <ul>
            <li><a href="https://www.linkedin.com/in/vuhongdoan/" target="_blank" rel="noopener">{SOCIAL_SVG['linkedin']}</a></li>
            <li><a href="mailto:dnvh.72@gmail.com">{SOCIAL_SVG['email']}</a></li>
          </ul>
        </div>
      </nav>
    </div>
  </div>
  <div class="site-wrap cfix">
    <div class="site-container">
      <div class="site-content">
        <div class="sidebar-content">
          <header class="site-header">
            <div class="logo-wrap">
              <div class="logo logo-image">
                <div class="image-normal image-link">
                  <a href="/"><img src="{LOGO}" alt="Vu-Hong Doan" /></a>
                </div>
              </div>
            </div>
            <div class="hamburger-click-area js-hamburger" role="button" aria-label="Open menu" tabindex="0">
              <div class="hamburger"><i></i><i></i><i></i></div>
            </div>
          </header>
          <nav>
            <ul class="group">{nav}</ul>
            <div class="link-title">
              <a href="https://drive.google.com/file/d/1loWXdPouvD5Cz0y9K4oYEMI8gLpN_6Ct/view?usp=sharing" target="_blank" rel="noopener">Resume</a>
            </div>
            <div class="social pf-nav-social">
              <ul>
                <li><a href="https://www.linkedin.com/in/vuhongdoan/" target="_blank" rel="noopener">{SOCIAL_SVG['linkedin']}</a></li>
                <li><a href="mailto:dnvh.72@gmail.com">{SOCIAL_SVG['email']}</a></li>
              </ul>
            </div>
          </nav>
        </div>
        <main>{main_body}</main>
      </div>
    </div>
  </div>
</body>
</html>"""


def gate_page() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="robots" content="noindex" />
  <title>Password Protected Page</title>
  <link rel="icon" href="/images/50f23401-291a-41b2-9212-2a3412ec5a14.png" />
  <link rel="stylesheet" href="/css/gate.css" />
  <script src="/js/config.js"></script>
  <script src="/js/gate.js" defer></script>
</head>
<body>
  <div class="password-form-content content">
    <form class="password-form js-password-form" id="gate-form">
      <input type="password" name="password" class="input-text js-password" autofocus placeholder="Enter password..." autocomplete="current-password" />
      <button type="submit" class="btn-password btn-submit js-btn-submit" disabled>Submit</button>
    </form>
    <p class="gate-error js-gate-error" hidden>Incorrect password. Please try again.</p>
  </div>
</body>
</html>"""


def write_page(out_path: Path, html: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html)


def main() -> None:
    meta = json.loads((CONTENT / "meta.json").read_text())

    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir()

    work_body = (CONTENT / "work.html").read_text()
    work_page = shell(meta["work"]["title"], "/work/", work_body)
    write_page(BUILD / "index.html", work_page)
    write_page(BUILD / "work" / "index.html", work_page)

    for slug, info in meta.items():
        if slug in ("home", "work"):
            continue
        body = (CONTENT / f"{slug}.html").read_text()
        page = shell(info["title"], SLUGS[slug], body)
        write_page(BUILD / slug / "index.html", page)

    write_page(BUILD / "gate.html", gate_page())
    (BUILD / "CNAME").write_text("vuhongdoan.com\n")

    for sub in ("css", "js", "images"):
        src = PUBLIC / sub
        if src.exists():
            shutil.copytree(src, BUILD / sub, dirs_exist_ok=True)

    # GitHub Pages serves from /site via workflow — also copy CNAME placeholder
    print(f"Built static site in {BUILD}/ ({len(list(BUILD.rglob('*')))} files)")


if __name__ == "__main__":
    main()
