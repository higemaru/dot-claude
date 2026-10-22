---
name: check-text
description: 誤字・脱字・用語統一をチェックする。文体の質的確認は /check-style、著作物確認は /check-copyright を使う。
context: fork
agent: Explore
---

## 他のチェックスキルとの使い分け
- /check-text      → 誤字・脱字・用語統一（機械的チェック）
- /check-style     → DNAとの乖離（文体・トーン・構造の質的チェック）
- /check-copyright → 著作物に関する確認（類似・引用）

## チェック手順
1. resources/style-guide.md を読み込む
   - 存在しない場合は「style-guide.md がありません。作成しますか？」と確認する
2. ~/.claude/rules/writing-workflow.md の「表記の既定ルール」節を読む
   - style-guide.md に別段の定義があれば、そちらを優先する
3. 指定されたファイル（なければ直近の編集ファイル）を対象にする
4. 以下の順でチェック:
   a. 誤字・脱字
   b. 用語の統一と表記（style-guide.md → 既定ルールの順に従う）
   c. style-guide.md に未定義の用語が出た場合は「要追加」として報告し、追加するか確認する
5. 問題があれば [行の特定] [種類] [内容] の形式で列挙
6. 問題なければ「チェック完了：問題なし」と一行で報告
