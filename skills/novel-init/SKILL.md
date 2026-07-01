---
name: novel-init
description: 小説プロジェクトを初期化する。テンプレートをコピーして作品タイトルと構成方針を設定する。
---

## 実行手順

1. 以下を順番に聞く（一度に聞かない）
   - 「作品タイトルを教えてください」
   - 「この話はどちらで終わりますか？
       - 余韻（情景・感情の残像で終わる）→ 序破急で構成
       - 解決（問題解決・主人公の変容で終わる）→ Save the Cat 15 beats で構成」

2. テンプレートをコピーする
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

7. resources/plot.md の ending_type を確定させる
   - 余韻 を選んだ場合：序破急テンプレートのみ残し、Save the Cat セクションを削除する
   - 解決 を選んだ場合：Save the Cat 15 beats テンプレートのみ残し、序破急セクションを削除する

8. 完了後、以下を案内する
   - 作成されたファイルの一覧
   - 選択した構成方針（余韻→序破急 / 解決→Save the Cat）
   - 次のステップ：
     - CLAUDE.md の「このプロジェクトについて」を書く
     - resources/characters.md に登場人物を書く
     - resources/plot.md のテンプレートを埋める
     - 書き始める準備ができたら manuscript/ に原稿ファイルを作る
