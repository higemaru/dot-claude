# 安全寄りの settings（たたき台）

Claude Code を「とりあえず触ってみる」段階で使う、最低限の設定です。
個人用の settings.json から私物（Hooks・ステータスライン・モデル指定・表示設定）を抜き、安全側の設定だけを残しています。

外せないようにしたいものを `managed-settings.json` に、あとから調整してよいものを `settings.json` に分けています。

## ファイル構成

| ファイル | 置き場所 | 書き換え |
|---|---|---|
| `managed-settings.json` | `/Library/Application Support/ClaudeCode/managed-settings.json` | root 権限が必要 |
| `settings.json` | `~/.claude/settings.json` | 自由に |
| `settings.merged.json` | `~/.claude/settings.json` | 自由に |

`settings.merged.json` は、上の 2 つを 1 つにまとめた自分用の版です。管理設定を置かない環境で、同じ内容を試すために使います。強制力はありません。

## 使い方

### 管理設定とユーザー設定に分けて置く

```bash
# 管理設定。root 権限で置く
sudo mkdir -p "/Library/Application Support/ClaudeCode"
sudo cp managed-settings.json "/Library/Application Support/ClaudeCode/managed-settings.json"

# ユーザー設定。既存の settings.json があると上書きするので、先に確認する
ls ~/.claude/settings.json
cp settings.json ~/.claude/settings.json
```

### 1 つにまとめて置く（自分用）

```bash
# 既存の settings.json があると上書きするので、先に確認する
ls ~/.claude/settings.json
cp settings.merged.json ~/.claude/settings.json
```

既存ファイルがある場合は、どちらも上書きせずに手動でマージします。

## 2 つの設定の重なり方

Claude Code は、ユーザー → プロジェクト → ローカル → CLI フラグ → 管理設定の順に設定を重ねます（v2.1.291 のバイナリで確認）。

- オブジェクトはキーごとに混ざる。ユーザー側の `sandbox` と管理設定側の `sandbox` は、片方がもう片方を丸ごと置き換えるのではなく、1 つの `sandbox` になる
- 同じキーがぶつかったら、最後に重なる管理設定が勝つ。ユーザーが `sandbox.enabled: false` と書いても有効のまま
- 配列（`deny` / `ask` / `allowedDomains` / `envVars` など）は連結される。ユーザー側から管理設定の deny を減らすことはできない

## `_dummy_key_` で始まるキー

検討中の項目を、効かない形で仮置きしています。Claude Code は知らないキーを無視するので、キー名の頭に `_dummy_key_` を付けると無効になります。有効にするときは `_dummy_key_` を外します。

- `_dummy_key_forceLoginOrgUUID`: ログインできる組織を限定する。組織の UUID が決まったら入れる
- `_dummy_key_autoApprove`: 仮置き。この名前の設定キーは Claude Code にはない
- `_dummy_key_Monitor`（deny の中）: `Monitor` ツールを止めるかどうか検討中。deny の配列の中にあるので、キーではなく「`_dummy_key_Monitor` というツールを拒否する」ルールとして読まれる

## managed-settings.json の各項目

### forceLoginMethod: "claudeai"

claude.ai のアカウント（Team / Pro / Max）でのログインに限定します。Console アカウントでのログインは選べなくなります。

### allowManagedHooksOnly: true

管理設定に書いた Hooks だけを動かします。ユーザー・プロジェクトの settings.json に書かれた Hooks は無視されます。

よそのアプリが `~/.claude/settings.json` に Hooks を書き込むことがあります（実例: iTerm2 の Claude Code 連携は、10 イベント分の Hooks を書き足し、アプリを削除したあとも残っていた）。これを防ぎます。

### allowManagedMcpServersOnly: true / allowedMcpServers: []

使ってよい MCP サーバーの一覧を、管理設定からだけ読みます。一覧が空なので、ユーザーは MCP サーバーを 1 つも使えません。claude.ai のコネクタ（Google Drive など）も対象です。

### disableSkillShellExecution: true

スキルやカスタムスラッシュコマンドに書かれたシェルの埋め込み実行を止めます。実行されずに、プレースホルダーに置き換わります。対象はユーザー・プロジェクト・プラグインのスキルで、管理設定で配るスキルと Claude Code 組み込みのスキルは対象外です。

### permissions.disableBypassPermissionsMode: "disable"

すべての確認を省略する bypassPermissions モードを使えなくします。

### permissions.deny

認証情報やシェルの設定・履歴を、Claude のツールから読み書きできないようにします。

- `Read` / `Edit`: すべての対象に書いている。Write / Glob / Grep はパスのルールが効かないので書いていない（Edit の 1 行でファイルを書き込むツールすべてに、Read の 1 行で Glob と Grep にも効く）
- Grep は、検索先が Read の deny に当たれば拒否され、親ディレクトリを検索したときも deny に当たるファイルは結果から除かれる（v2.1.292 のバイナリで確認）

ホームディレクトリ配下の認証情報（`~/.ssh`、`~/.aws`、`~/.config/gh`、`~/.kube`、`~/Library/Keychains` など）に加えて、プロジェクト内の `.env` や鍵ファイルも、`**/` を付けてサブディレクトリまで含めて対象にしています。`**/*.key` は Keynote の書類（`.key`）にもマッチしますが、Claude が Keynote を読むことはまずないので、そのままにしています。

`WebSearch` と `WebFetch` も止めています。この 2 つは Claude Code 本体のツールで、sandbox の `allowedDomains` の対象外です。GitHub だけに絞った通信の制限が、この 2 つには効きません。

git の操作のうち、取り返しのつかないものも deny にしています。

- `git push`（すべて）: sandbox の中からは `~/.ssh` が読めず、SSH での push はどのみちできません。push は人間が行います
- `git reset --hard` / `git clean -f`: 作業中の変更を消す操作

### sandbox.enabled: true / sandbox.allowUnsandboxedCommands: false

Bash コマンドを macOS の sandbox の中で実行します。`allowUnsandboxedCommands: false` で、Claude が sandbox を外してコマンドを実行する手段（`dangerouslyDisableSandbox`）も無効にします。すべてのコマンドが sandbox の中で動きます。

ユーザーが外せないよう、この 2 つだけ管理設定に置いています。sandbox のほかの項目はユーザー設定にあります。

`permissions.deny` の Read ルールは sandbox の `filesystem.denyRead` に合算されるので、認証情報のファイルは Bash の `cat` などからも読めません。そのため `credentials.files` は書いていません。

## settings.json の各項目

### $schema

エディタで settings.json を開いたときに、キーの補完や誤りの指摘を受けられるようにします。動作には影響しません。

### language: "Japanese"

Claude の応答を日本語にします。

### cleanupPeriodDays: 365

会話ログを手元に残す日数です（既定は 30 日）。ふりかえりや調査のために 1 年残します。
会話ログにはコマンドの出力もそのまま入るので、画面に出た情報は 1 年間 `~/.claude/projects/` に残ります。認証情報などを画面に出さない運用とセットで考えてください。

### env

Claude Code の利用状況やエラーの情報を Anthropic に送らないようにします。

- `DISABLE_TELEMETRY`: 利用状況の送信を止める
- `DISABLE_ERROR_REPORTING`: エラー報告の送信を止める
- `DISABLE_FEEDBACK_COMMAND` / `DISABLE_BUG_COMMAND`: 会話の内容を添えて不具合を報告する `/feedback`（別名 `/bug`）コマンドを無効にする。どちらか 1 つでも止まるが、両方書いている

### permissions.defaultMode: "acceptEdits"

ファイルの編集と、よく使うファイル操作のコマンドを自動で承認します。sandbox を有効にしているので、sandbox の中で動く Bash コマンドも確認なしで実行されます（下の sandbox の節を参照）。
確認が出るのは、ask ルールに当たったとき、許可していないドメインに通信するとき、などに絞られます。慣れてきたら `auto`（別のモデルが操作を審査し、低リスクのものを自動実行する）を検討します。

### permissions.ask

実行前に必ず確認を出すコマンドです。`auto` モードでも ask ルールが優先されます。

- `rm` すべて（単発の削除も含む。git を使わない作業では消したファイルを戻せないので、削除は安全寄りにしている）
- `sudo`

ルールは前方一致の文字列マッチで、フラグの解析はしません。`/bin/rm` や `find -delete` などはすり抜けるので、これは減速帯です。本当の壁は sandbox と、Claude Code に組み込まれた rm の安全チェック（ホームやシステムのディレクトリを消す rm は人間の承認が必須）です。

### permissions.blockReadsOutsideWorkingDirectories: true

作業ディレクトリの外にあるファイルを、Read / Grep / Glob で読めなくします（どのモードでも）。`/etc` や `/var/log` を見せたい場合は、`permissions.additionalDirectories` で追加します（空の配列を置いてあります）。Bash の `cat` はこの設定の対象外です。

### sandbox

sandbox の有効化は管理設定にあります。ここには、あとから調整してよい項目を置いています。

sandbox の中で動く Bash コマンドは、確認なしで自動実行されます（`autoAllowBashIfSandboxed: true`。省略したときの既定値も `true`）。ただし、自動で許可する前に必ず deny ルールと ask ルールが照合されるので、rm・sudo・git push などは止まります。

確認が毎回出ると、中身を読まずに承認する癖がつきやすくなります。sandbox で被害の範囲を囲ったうえで確認を減らし、**確認が出たら立ち止まる**、という使い方を身につけるための設定です。自動で実行されたコマンドも画面には表示されるので、Claude が何をしたかは確認できます。

すべての Bash コマンドで確認を出したい場合は、`autoAllowBashIfSandboxed` を `false` に書き換えます。

- `filesystem`: sandbox の中での読み書きの範囲を追加・制限する。追加する場所がわかるよう、空の配列を置いてある
  - `allowWrite` / `denyWrite`: 書き込みを許可・拒否するパス（Edit の allow / deny ルールのパスと合算される）
  - `denyRead` / `allowRead`: 読み取りを拒否するパスと、その中で例外的に許可するパス（Read の deny ルールのパスと合算される）
- `credentials.envVars`: API キーやトークンの環境変数を、Bash コマンドに渡さない
- `network.allowedDomains`: 確認なしで通信してよいドメイン。ここにないドメインに繋ごうとすると確認が出る（即ブロックではない）

GitHub だけを許可しているので、それ以外の外部サービスや、ローカルネットワーク内のサーバーに繋ぐ場面で確認が出ます。Claude がどこに通信しようとしているかを、その場で見るための設定です。
GitHub 上のスクリプトを `curl ... | sh` で実行する形は、確認なしで sandbox の中で動きます。sandbox の外には出られないので、被害は作業ディレクトリの中に限られます。

## settings.merged.json について

2 つのファイルを、Claude Code と同じ規則（オブジェクトはキーごと、配列は連結）で 1 つにまとめたものです。違いは次の 2 点です。

- `allowManagedHooksOnly` と `allowManagedMcpServersOnly` は、管理設定に置いたときだけ効く。ユーザー設定では読まれないので、`_dummy_key_` を付けて無効にしている
- 管理設定に置いた項目も、自分で書き換えられる。deny も sandbox も「Claude には外させない」止まりで、「人には外させない」にはならない

`WebSearch` / `WebFetch` の deny と `allowedMcpServers: []` はそのまま残しています。自分用で調べものや MCP を使いたい場合は、使いながら外してください。

## 未確認

- `**/.env` のように `**` を含む Read ルールが、sandbox の `denyRead` に正しく変換されるか（Bash の `cat .env` が止まるか）。止まらない場合は、プロジェクト側の `.claude/settings.json` の `sandbox.credentials.files` で指定する（ユーザー設定で相対パスを書くと `~/.claude` 基準になるため）
- `settings.merged.json` で、`allowedMcpServers` がユーザー設定から読まれるか。読まれる場合は、claude.ai のコネクタを含めて MCP が使えなくなる
- `settings.merged.json` で、`forceLoginMethod` がログイン時に強制されるか。ユーザー設定からも読む箇所と、管理設定からしか読まない箇所が混在している
- deny の `_dummy_key_Monitor` のような、存在しないツール名のルールが警告だけで済むか

## 未検討

- よく使うドメインを `allowedDomains` に追加するか
