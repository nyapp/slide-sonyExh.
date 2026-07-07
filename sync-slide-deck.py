#!/usr/bin/env python3
"""
プロジェクト直下の「三桁数字で始まる .html」を名前順で列挙し、
index.html 内の <!-- SLIDE_DECK_URLS:BEGIN --> … END ブロックを更新する。
ブラウザはローカルディレクトリを列挙できないため、この同期がデッキの正とする。
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRESENT = ROOT / "index.html"
SLIDE_NAME = re.compile(r"^\d{3}-.+\.html$")
# デッキには載せずファイルだけ残すスライド
DECK_EXCLUDE = frozenset({"080-theATeam.html"})
MARKERS = re.compile(
    r"^[ \t]*<!-- SLIDE_DECK_URLS:BEGIN -->.*?^[ \t]*<!-- SLIDE_DECK_URLS:END -->",
    re.DOTALL | re.MULTILINE,
)


def collect_slides() -> list[str]:
    names: list[str] = []
    for p in ROOT.iterdir():
        if p.is_file() and SLIDE_NAME.match(p.name) and p.name not in DECK_EXCLUDE:
            names.append(p.name)
    names.sort()
    return names


def build_embed_block(urls: list[str]) -> str:
    lines = [
        "    <!-- SLIDE_DECK_URLS:BEGIN -->",
        "    <script>",
        "    window.__SLIDE_DECK_URLS__ = [",
    ]
    for u in urls:
        lines.append(f'        "{u}",')
    lines.append("    ];")
    lines.append("    </script>")
    lines.append("    <!-- SLIDE_DECK_URLS:END -->")
    return "\n".join(lines)


def main() -> None:
    urls = collect_slides()
    block = build_embed_block(urls)
    text = PRESENT.read_text(encoding="utf-8")
    if not MARKERS.search(text):
        raise SystemExit(f"マーカーが見つかりません: {PRESENT}")
    new_text = MARKERS.sub(block, text, count=1)
    PRESENT.write_text(new_text.replace("\r\n", "\n"), encoding="utf-8")
    print(f"{PRESENT.name}: {len(urls)} 枚を反映しました。")


if __name__ == "__main__":
    main()
