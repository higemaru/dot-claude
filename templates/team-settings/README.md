# 教育用 settings.json（たたき台）

Claude Code を「とりあえず触ってみる」段階で配る、最低限の `~/.claude/settings.json` です。
個人用の settings.json から私物（Hooks・ステータスライン・モデル指定・表示設定）を抜き、安全側の設定だけを残しています。

## 使い方

`~/.claude/settings.json` がまだない場合は、そのままコピーします。

```bash
# 既存の settings.json があると上書きするので、先に確認する
ls ~/.claude/settings.json
cp settings.json ~/.claude/settings.json
```

既存ファイルがある場合は、上書きせずに手動でマージします。

## 各項目の意味

### permissions.defaultMode: "acceptEdits"

ファイルの編集と、よく使うファイル操作のコマンドを自動で承認します。sandbox を有効にしているので、sandbox の中で動く Bash コマンドも確認なしで実行されます（下の sandbox の節を参照）。
確認が出るのは、ask ルールに当たったとき、許可していないドメインに通信するとき、などに絞られます。慣れてきたら `auto`（別のモデルが操作を審査し、低リスクのものを自動実行する）を検討します。

### permissions.disableBypassPermissionsMode: "disable"

すべての確認を省略する bypassPermissions モードを使えなくします。

### permissions.ask

実行前に必ず確認を出すコマンドです。`auto` モードでも ask ルールが優先されます。

- `rm` すべて（単発の削除も含む。git を使わない作業では消したファイルを戻せないので、削除は安全寄りにしている）
- `sudo`
- `git push`（`--force` / `-f` を含むすべて）/ `git reset --hard` / `git clean -f`
- `curl` / `wget` の出力をパイプで `sh` に渡す形（`curl ... | sh` など）

ルールは前方一致の文字列マッチで、フラグの解析はしません。`/bin/rm` や `find -delete` などはすり抜けるので、これは減速帯です。本当の壁は下の sandbox と、Claude Code に組み込まれた rm の安全チェック（ホームやシステムのディレクトリを消す rm は人間の承認が必須）です。

`curl *|*sh*` は、パイプの後ろに `sh` を含むコマンドすべてにマッチします（`| shasum` や `| grep ssh` も対象）。誤検出があるので deny ではなく ask にしています。確認が出たら、中身を見て承認してください。

### permissions.deny

認証情報やシェルの設定・履歴を、Claude の Read / Edit / Grep ツールから読み書きできないようにします。
Write と Glob はパスのルールが効かないので書いていません（Edit の 1 行で、ファイルを書き込むツールすべてに効きます）。

プロジェクト内の `.env` / `.env.*` / `secrets/` も、`**/` を付けてサブディレクトリまで含めて対象にしています。ただし、これは Claude のツールにしか効きません。Bash の `cat .env` は止まらないので、塞ぐ場合はプロジェクト側の `.claude/settings.json` の `sandbox.credentials.files` で指定します（ユーザー設定で相対パスを書くと、`~/.claude` 基準になるため）。

### permissions.blockReadsOutsideWorkingDirectories: true

作業ディレクトリの外にあるファイルを、Read / Grep / Glob で読めなくします（どのモードでも）。`/etc` や `/var/log` を見せたい場合は、`permissions.additionalDirectories` で追加します（空の配列を置いてあります）。Bash の `cat` はこの設定の対象外です。

### sandbox

Bash コマンドを macOS の sandbox の中で実行します。

sandbox の中で動く Bash コマンドは、確認なしで自動実行されます（`autoAllowBashIfSandboxed: true`。省略したときの既定値も `true`）。ただし、自動で許可する前に必ず deny ルールと ask ルールが照合されるので、rm・sudo・push・`curl | sh` などは確認が出ます。

確認が毎回出ると、中身を読まずに承認する癖がつきやすくなります。sandbox で被害の範囲を囲ったうえで確認を減らし、**確認が出たら立ち止まる**、という使い方を身につけるための設定です。自動で実行されたコマンドも画面には表示されるので、Claude が何をしたかは確認できます。

すべての Bash コマンドで確認を出したい場合は、`autoAllowBashIfSandboxed` を `false` に書き換えます。

- `filesystem`: sandbox の中での読み書きの範囲を追加・制限する。追加する場所がわかるよう、空の配列を置いてある
  - `allowWrite` / `denyWrite`: 書き込みを許可・拒否するパス（Edit の allow / deny ルールのパスと合算される）
  - `denyRead` / `allowRead`: 読み取りを拒否するパスと、その中で例外的に許可するパス（Read の deny ルールのパスと合算される）
- `credentials.files`: deny と同じファイルを、Bash コマンド（`cat` など）からも読めなくする
- `credentials.envVars`: API キーやトークンの環境変数を、Bash コマンドに渡さない
- `network.allowedDomains`: 確認なしで通信してよいドメイン。ここにないドメインに繋ごうとすると確認が出る（即ブロックではない）
- `allowUnsandboxedCommands: false`: Claude が sandbox を外してコマンドを実行する手段（`dangerouslyDisableSandbox`）を無効にする。すべてのコマンドが sandbox の中で動く

GitHub と npm・PyPI だけを許可しているので、それ以外の外部サービスや社内サーバーに繋ぐ場面で確認が出ます。Claude がどこに通信しようとしているかを、その場で見るための設定です。

sandbox の中からは `~/.ssh` が読めないため、SSH での `git push` は Claude からは実行できません。push は人間が行います。

## 未検討

- 社内で使うドメインを `allowedDomains` に追加するか
- 本格導入時の管理設定（managed-settings.json）との分担
