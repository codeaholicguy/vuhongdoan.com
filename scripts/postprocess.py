#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

THEME_CSS = "https://cdn.myportfolio.com/5e478d47-4994-45c3-97a6-cf213e06e0aa/419da4eaa6bf7b905f7feae8d230317b1783081893.css?h=dea122d900caa7ba9b2d551337130b87"


def patch_html(path: Path) -> None:
    html = path.read_text()
    html = html.replace(THEME_CSS, "/dist/css/theme.css")
    html = re.sub(
        r'src="/site/translations\?cb=[^"]+"',
        'src="/site/translations.js"',
        html,
    )
    html = re.sub(
        r'src="/dist/js/main\.js\?cb=[^"]+"',
        'src="/dist/js/main.js"',
        html,
    )
    path.write_text(html)
    print(f"Patched {path.relative_to(ROOT)}")


def main() -> None:
    for path in ROOT.rglob("*.html"):
        patch_html(path)


if __name__ == "__main__":
    main()
