#!/usr/bin/env python3
"""Download CDN assets and prepare HTML content for static hosting."""
from __future__ import annotations

import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGACY = ROOT / "legacy"
PUBLIC_IMAGES = ROOT / "public" / "images"
CONTENT = ROOT / "content"
PUBLIC_CSS = ROOT / "public" / "css"

PAGES = {
    "home": LEGACY / "index.html",
    "work": LEGACY / "work" / "index.html",
    "klarna-live-shopping": LEGACY / "klarna-live-shopping" / "index.html",
    "klarna-desktop-store-app": LEGACY / "klarna-desktop-store-app" / "index.html",
    "tiki-rewards-program": LEGACY / "tiki-rewards-program" / "index.html",
    "gamify-users-journey-on-tiki": LEGACY / "gamify-users-journey-on-tiki" / "index.html",
    "aeho-product-information-management-solution": LEGACY
    / "aeho-product-information-management-solution"
    / "index.html",
}


def parse_dimension(url: str) -> int:
    name = url.split("/")[-1].split("?")[0]
    numbers = [int(n) for n in re.findall(r"x(\d+)", name)]
    if len(numbers) >= 2:
        return numbers[-2] * numbers[-1]
    return numbers[-1] if numbers else 0


def pick_best_urls(html: str) -> dict[str, str]:
    best: dict[str, tuple[int, str]] = {}
    for url in re.findall(r"https://cdn\.myportfolio\.com/[^\"'\s>)]+", html):
        match = re.search(
            r"/([0-9a-f-]{36})_[^./?]+\.(png|jpe?g|gif|webp)", url, re.I
        )
        if not match:
            continue
        asset_id = match.group(1)
        score = parse_dimension(url)
        if asset_id not in best or score > best[asset_id][0]:
            best[asset_id] = (score, url)
    return {asset_id: data[1] for asset_id, data in best.items()}


def download_one(asset_id: str, url: str) -> tuple[str, bool, str]:
    ext_match = re.search(r"\.(png|jpe?g|gif|webp)", url, re.I)
    suffix = (ext_match.group(1).lower() if ext_match else "png").replace("jpeg", "jpg")
    dest = PUBLIC_IMAGES / f"{asset_id}.{suffix}"
    if dest.exists() and dest.stat().st_size > 0:
        return asset_id, True, f"cached {dest.name}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=90) as resp:
            dest.write_bytes(resp.read())
        return asset_id, True, f"{dest.name} ({dest.stat().st_size // 1024}KB)"
    except Exception as exc:
        return asset_id, False, str(exc)


def local_image_path(asset_id: str, url: str) -> str:
    ext_match = re.search(r"\.(png|jpe?g|gif|webp)", url, re.I)
    suffix = (ext_match.group(1).lower() if ext_match else "png").replace("jpeg", "jpg")
    return f"images/{asset_id}.{suffix}"


def fix_internal_links(html: str) -> str:
    for slug in PAGES:
        if slug == "home":
            continue
        html = re.sub(rf'href="/{re.escape(slug)}/?"', f'href="{slug}/"', html)
    return html


def replace_cdn_urls(html: str, best_urls: dict[str, str]) -> str:
    for asset_id, cdn_url in best_urls.items():
        local = local_image_path(asset_id, cdn_url)
        html = re.sub(
            rf"https://cdn\.myportfolio\.com/[^\"'\s>]*/{re.escape(asset_id)}_[^\"'\s>]+",
            local,
            html,
        )
    html = re.sub(r'\sdata-src="[^"]*"', "", html)
    html = re.sub(r'\sdata-srcset="[^"]*"', "", html)
    html = re.sub(r'\sdata-sizes="[^"]*"', "", html)
    html = re.sub(r"\sjs-lazy", "", html)
    return html


def extract_main(html: str) -> str:
    match = re.search(r"<main>(.*)</main>", html, re.S)
    if not match:
        raise ValueError("No <main> block found")
    return match.group(1).strip()


def extract_title(html: str) -> str:
    match = re.search(r"<title>([^<]+)</title>", html)
    return match.group(1).strip() if match else "Vu Hong Doan"


def main() -> None:
    PUBLIC_IMAGES.mkdir(parents=True, exist_ok=True)
    CONTENT.mkdir(parents=True, exist_ok=True)
    PUBLIC_CSS.mkdir(parents=True, exist_ok=True)

    combined = "\n".join(p.read_text() for p in PAGES.values() if p.exists())
    best_urls = pick_best_urls(combined)

    print(f"Downloading {len(best_urls)} images...")
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(download_one, aid, url) for aid, url in best_urls.items()]
        for fut in as_completed(futures):
            aid, ok, msg = fut.result()
            print(("  OK " if ok else "  FAIL ") + f"{aid}: {msg}")

    for name, src in [("main.css", LEGACY / "dist/css/main.css"), ("theme.css", LEGACY / "dist/css/theme.css")]:
        if src.exists():
            (PUBLIC_CSS / name).write_bytes(src.read_bytes())

    meta = {}
    for slug, path in PAGES.items():
        if not path.exists():
            continue
        main_html = fix_internal_links(
            replace_cdn_urls(extract_main(path.read_text()), best_urls)
        )
        (CONTENT / f"{slug}.html").write_text(main_html)
        meta[slug] = {"title": extract_title(path.read_text())}

    (CONTENT / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"Prepared {len(meta)} content files.")


if __name__ == "__main__":
    main()
