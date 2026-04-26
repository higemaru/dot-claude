---
name: novel-init
description: 小説プロジェクトを初期化する。テンプレートをコピーして作品タイトルを設定する。
---

## 実行手順

1. 「作品タイトルを教えてください」と聞く

2. 以下のコマンドでテンプレートをコピーする
```bash
cp -r ~/.claude/templates/novel/. .
```

3. CLAUDE.local.md をコピーする
```bash
cp ~/.claude/templates/novel/CLAUDE.local.md .
```

4. .gitignore を作成する
```bash
cat > .gitignore << 'EOF'
CLAUDE.local.md
EOF
```

5. コピーしたファイル内のプレースホルダーを置換する
```bash
TITLE="（入力されたタイトル）"
find . -name "*.md" | xargs sed -i "" "s/{{タイトル}}/${TITLE}/g"
find . -name "*.md" | xargs sed -i "" "s/{{作品タイトル}}/${TITLE}/g"
```

6. manuscript/ と materials/ ディレクトリを作成する
```bash
mkdir -p manuscript materials
```

7. 完了後、以下を案内する
   - 作成されたファイルの一覧
   - 次のステップ：
     - CLAUDE.md の「このプロジェクトについて」を書く
     - resources/characters.md に登場人物を書く
     - resources/plot.md で Save the Cat 15 beat を埋める
     - 書き始める準備ができたら manuscript/ に原稿ファイルを作る
