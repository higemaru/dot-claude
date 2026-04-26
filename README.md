# Claude Code 執筆セットアップ

## インストール（一度だけ）

```bash
# このディレクトリの中身を ~/.claude/ にコピーする
# ※ settings.json が既にある場合は手動でマージする
cp -r . ~/.claude/
```

### settings.json のマージ
既存の settings.json がある場合は、`"hooks"` ブロックを既存ファイルに追記してください。

---

## ディレクトリ構成

```
~/.claude/
  CLAUDE.md              グローバル習慣・共通ルール
  settings.json          Hooks設定（起動時表示・文字数カウント）
  README.md              このファイル
  skills-reference.md    スキル一覧早見表
  statusline-command.sh  ステータスライン表示スクリプト
  rules/
    novel-dna.md         小説の作風DNA
    technical-dna.md     技術書の作風DNA
  scripts/
    export-transcript.py 会話トランスクリプトをMarkdownに変換
  skills/
    novel-init/          /novel-init  小説プロジェクト初期化
    tech-init/           /tech-init   技術書プロジェクト初期化
    brainstorm/          /brainstorm  アイデア出し
    outline/             /outline     章立て作成（技術書）
    draft/               /draft       初稿生成
    polish/              /polish      推敲
    synopsis/            /synopsis    あらすじ生成
    check-text/          /check-text  誤字・用語チェック
    check-style/         /check-style 文体チェック
    check-copyright/     /check-copyright 著作権チェック
    end/                 /end         セッション終了・トランスクリプト保存
  templates/
    novel/               /novel-init のコピー元
    technical/           /tech-init のコピー元
```

---

## 新規プロジェクトの始め方

### 小説
```bash
mkdir project-name && cd project-name
claude
> /novel-init
```

### 技術書
```bash
mkdir project-name && cd project-name
claude
> /tech-init
```

## 執筆中

```
> /check-text … 誤字・脱字・用語統一チェック
> /end … セッション終了時の引き継ぎ作成
```

---

## Hooks の動作

settings.json 内で定義。Hooks は「依頼・お願い」ではなく「指示」です。必ず実行されます。

| タイミング | 動作 |
|---|---|
| セッション開始時 | progress.md と todo.md を表示 |
| 原稿ファイル編集後 | 文字数を表示（非同期） |
| Claudeが応答を終えるたび | progress.md にタイムスタンプを記録（非同期） |

## Ctrl+D で終了した場合

Stop hook が毎ターン progress.md を更新しているため、次回 SessionStart 時に前回の状態が復元されます。ただし `/end` を使った終了より情報量が少なくなります。

---

## トランスクリプトの保存

`/end` スキルが自動的に実行しますが、任意のタイミングで手動実行も可能です。

```bash
python3 ~/.claude/scripts/export-transcript.py <project_dir> [output_dir]
```

- `project_dir`: プロジェクトのルートディレクトリ（絶対パス）
- `output_dir`: 出力先（省略時は `project_dir/transcripts/`）

Claude Code が保存する会話 JSONL（`~/.claude/projects/<encoded-path>/*.jsonl`）を読み込み、`YYYY-MM-DD_セッションID.md` という名前の Markdown ファイルに変換します。同名ファイルが存在する場合は上書きします。

**動作環境:** macOS / Linux（Python 3.7 以上）
