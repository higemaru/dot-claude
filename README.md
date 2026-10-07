# Claude Code 執筆セットアップ

## インストール（一度だけ）

### 初めて Claude Code を使う場合

`~/.claude/` がまだない場合は、このディレクトリの中身をそのままコピーします。

```bash
cp -r . ~/.claude/
```

### すでに Claude Code を使っている場合

`~/.claude/` に既存の `CLAUDE.md` や `settings.json` がある状態で `cp -r . ~/.claude/` を実行すると、既存のカスタマイズを上書きして消してしまいます。個別にコピーし、重複するファイルは手動でマージします。

```bash
cp -r rules context scripts skills templates ~/.claude/
cp skills-reference.md statusline.py ~/.claude/
```

- `CLAUDE.md`: このリポジトリの内容を参考に、必要な箇所だけ既存ファイルに追記する
- `settings.json`: `"hooks"` ブロックを既存ファイルに追記する

------

## ディレクトリ構成

```
~/.claude/
  CLAUDE.md              グローバル設定（汎用のみ・口調と共通動作指示）
  settings.json          Hooks / サンドボックス / 権限設定
  README.md              このファイル
  skills-reference.md    スキル一覧早見表
  statusline.py          ステータスライン表示スクリプト
  rules/
    writing-workflow.md  役割・執筆の進め方・セッション管理（執筆プロジェクトが import）
    novel-dna.md         小説の作風DNA
    technical-dna.md     技術書の作風DNA
    private/             非公開ファイル置き場（.gitignoreで丸ごと除外）
      character_sheet.md Claudeの性格・口調（任意・非公開。あれば口調のデフォルトより優先）
  context/
    persona.md           ユーザーの人となり・好み・価値観（任意・非公開）
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

------

## 性格・ユーザー情報のカスタマイズ（任意）

`rules/private/character_sheet.md` と `context/persona.md` は、このリポジトリでは追跡していません。
（`.gitignore` で除外済み）個人用ファイルです。存在する場合のみ `CLAUDE.md` から参照されます。

- `rules/private/character_sheet.md`: Claude自身の性格・口調。存在すれば `CLAUDE.md` の「口調」のデフォルトより優先される
- `context/persona.md`: ユーザーの人となり・好み・価値観。Claudeがユーザーに合わせた対応をするための参考情報

必要であれば自分で作成してください。公開リポジトリなので、機微な情報を書く場合は非公開のままにしておいてください。

------

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

------

## 執筆中

```
> /check-text … 誤字・脱字・用語統一チェック
> /end … セッション終了時の引き継ぎ作成
```

------

## Hooks の動作

settings.json 内で定義。Hooks は「依頼・お願い」ではなく「指示」です。必ず実行されます。

| タイミング         | 動作                          |
| ------------------ | ----------------------------- |
| セッション開始時   | progress.md と todo.md を表示 |
| 原稿ファイル編集後 | 文字数を表示（非同期）        |

------

## Ctrl+D で終了した場合

progress.md / todo.md の更新は `/end` スキルが担っています。`/end` を実行せずに `Ctrl+D` で抜けると、前回 `/end` を実行した時点までしか記録が残りません。セッションを終える時は `/end` を使うことを推奨します。

------

## トランスクリプトの保存

`/end` スキルが自動的に実行しますが、任意のタイミングで手動実行も可能です。

```bash
python3 ~/.claude/scripts/export-transcript.py <project_dir> [output_dir]
```

- `project_dir`: プロジェクトのルートディレクトリ（絶対パス）
- `output_dir`: 出力先（省略時は `project_dir/transcripts/`）

Claude Code が保存する会話 JSONL（`~/.claude/projects/<encoded-path>/*.jsonl`）を読み込み、`YYYY-MM-DD_セッションID.md` という名前の Markdown ファイルに変換します。同名ファイルが存在する場合は上書きします。

**動作環境:** macOS / Linux（Python 3.7 以上）