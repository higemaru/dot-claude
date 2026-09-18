---
name: tech-init
description: 技術書プロジェクトを初期化する。テンプレートをコピーして書籍タイトルを設定する。
---

## 実行手順

1. 以下を順番に聞く（一度に聞かない）
   - 「書籍タイトルを教えてください」
   - 「この本のキーワードを一言で教えてください（例: 偏愛・安逸・常楽）」

2. 以下のコマンドでテンプレートをコピーする（CLAUDE.local.md も一緒に入る）
```bash
cp -r ~/.claude/templates/technical/. .
```


3. .gitignore を作成する
```bash
cat > .gitignore << 'EOF'
CLAUDE.local.md
EOF
```

4. コピーしたファイル内のプレースホルダーを置換する
```bash
TITLE="（入力されたタイトル）"
KEYWORD="（入力されたキーワード）"
find . -name "*.md" | xargs sed -i "" "s/{{タイトル}}/${TITLE}/g"
find . -name "*.md" | xargs sed -i "" "s/{{書籍タイトル}}/${TITLE}/g"
find . -name "*.md" | xargs sed -i "" "s/{{偏愛・安逸・常楽など}}/${KEYWORD}/g"
```

5. chapters/ と references/ ディレクトリを作成する
```bash
mkdir -p chapters references
```

6. 完了後、以下を案内する
   - 作成されたファイルの一覧
   - 次のステップ：
     - CLAUDE.md の「ターゲット読者」「ゴール」を書く
     - /outline で章立てを対話的に作る
     - まえがきから書き始める（動機・自己紹介・キーワード提示の順）
