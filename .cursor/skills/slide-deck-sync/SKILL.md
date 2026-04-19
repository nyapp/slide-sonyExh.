---
name: slide-deck-sync
description: >-
  Syncs the embedded slide deck list in index.html from all root-level
  NNN-*.html files via sync-slide-deck.py. Use when the user adds, removes, or
  renames three-digit-prefixed slide HTML files, when index.html deck order is
  wrong or empty, or when they mention syncing slides / プレゼン用デッキ /
  sync-slide-deck.
---

# スライドデッキ同期（slide リポジトリ）

## いつ実行するか

- 直下に `000-foo.html` のような **三桁数字で始まる** スライドを追加・削除・リネームしたあと
- `index.html` を開いたとき **枚数や順序が古い** とき
- ユーザーが「デッキを同期」「manifest」「スライド一覧」などと言ったとき

## 手順

1. リポジトリ直下（`sync-slide-deck.py` と同じディレクトリ）にいることを確認する。
2. 次を **そのまま実行**する（標準ライブラリのみ。仮想環境不要）。

```bash
python3 sync-slide-deck.py
```

3. 成功時は `index.html: N 枚を反映しました。` のような一行が出る。
4. 失敗時はマーカー欠落などのメッセージを読み、`index.html` 内の  
   `<!-- SLIDE_DECK_URLS:BEGIN -->` … `END` が存在するか確認する。

## ルール（エージェント向け）

- **対象ファイル名**: `^\d{3}-.+\.html$` に一致する **直下のファイルのみ**。`index.html` は命名上含まれない。
- **並び順**: ファイル名の **文字列としての昇順**（`010-` は `020-` の前）。
- **ブラウザはディレクトリ列挙できない**ため、一覧の正はこのスクリプト更新後の `index.html` 埋め込みブロックとする。手で `__SLIDE_DECK_URLS__` を編集してもよいが、次回同期で上書きされる。

## ユーザー向け一言

プレゼン用の連続表示は `index.html`（ディレクトリの既定ページとしても開ける）。スライド HTML を変えたら上記コマンドを一度実行する。
