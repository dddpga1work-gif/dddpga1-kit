# dddpga1 Dev Kit (`dddpga1-kit`)

個人用のグローバル開発ルール（`AGENTS.md`）、Web開発・ブラウザ起動スキル、および危険コマンド検知・防御Hookを1つに統合した **Google Antigravity プラグイン**です。

---

## 📦 ディレクトリ構成

```text
dddpga1-kit/
├── plugin.json                # プラグインマニフェスト
├── hooks.json                 # ライフサイクルHook定義
├── hooks/
│   └── safety-gate.py         # PreToolUse (run_command) 用のコマンド安全ゲートスクリプト
├── rules/
│   └── AGENTS.md              # 常時適用されるグローバル行動・開発ルール
└── skills/
    ├── commit/
    │   └── SKILL.md           # git commit 専用スキル
    ├── create-sp-layout/
    │   └── SKILL.md           # Web系SPレイアウト一発作成スキル
    ├── init-web-contents/
    │   └── SKILL.md           # Web系プロジェクト初期構築スキル
    └── start-browser/
        └── SKILL.md           # WSL2環境向け CDPモード Chrome起動スキル
```

---

## 🚀 インストール（導入方法）

### 1. グローバルプラグインとして導入する場合（推奨）

すべてのプロジェクト・ワークスペースで共通利用する場合は、`~/.gemini/config/plugins/` 配下にクローンします。

```bash
mkdir -p ~/.gemini/config/plugins
git clone https://github.com/dddpga1work-gif/dddpga1-kit.git ~/.gemini/config/plugins/dddpga1-kit
```

### 2. 特定のプロジェクト（ワークスペース）のみに導入する場合

プロジェクトルートの `.agents/plugins/` 配下に配置します。

```bash
mkdir -p .agents/plugins
git clone https://github.com/dddpga1work-gif/dddpga1-kit.git .agents/plugins/dddpga1-kit
```

### 前提条件
- **Python 3**: `hooks/safety-gate.py` の実行に使用します。
- **Google Chrome / Chromium**（WSL2環境で `/start-browser` を使用する場合）: `google-chrome-stable` または `chromium-browser` がインストールされている必要があります。

---

## 🧩 同梱コンポーネント詳細

### 1. グローバルルール (`rules/AGENTS.md`)

プラグイン有効時に常時適用される開発・行動原則です。

- **日本語対応**: ユーザーとのやり取りおよび表示はすべて日本語で行う。
- **コンテナ完結原則**: すべてのプロジェクトは他者への共有を想定し、`docker-compose up -d` 等で一発起動でき、コンテナ内で完結してローカル環境を一切汚さない構成とする。
- **事前確認の徹底**: 不明点は必ず事前にユーザーへ説明・確認を取ってから実行に移す。
- **修正後の全体精査**: エラー修正や改修後は全体を精査し、副作用・不整合・仕様破壊がないか確認して報告する。
- **最新仕様・公式ドキュメントの調査必須**: 古い知識や決めつけによる回答を禁止し、必ずWebや公式ドキュメントの最新版を調査してから回答・実装する。
- **根源治療とモダン技術選定**: 対症療法を禁止し、最新仕様に沿った根源的解決を行う。jQuery等のレガシー技術の利用は一切禁止。
- **コマンド待機とタスク管理**: 通常コマンド実行時は `WaitMsBeforeAsync` を最大値（`10000`ms）に設定して安易なバックグラウンド化を防ぎ、バックグラウンドタスクを放置したままターンを終了しない。
- **WSL2 Browser Subagent ルール**: WSL2環境で `browser_subagent` を使用する前に、必ず `/start-browser` を実行して Chrome/Chromium を CDP モードで起動する。

---

### 2. スキル一覧 (`skills/*/SKILL.md`)

チャット上で `/スキル名` または自然言語での指示により呼び出せます。

| スキル | 概要 | 主な挙動・仕様 |
| :--- | :--- | :--- |
| `/commit` | `git commit` 専用スキル | ・実装毎・機能毎にコミットメッセージ案を提案<br>・ユーザーが承諾した場合のみ `git commit` を実行<br>・**`git push` は絶対に行わない** |
| `/create-sp-layout` | Web系SPレイアウト作成 | ・既存のPCレイアウトに一切影響を与えず、メディアクエリ等のモダンな手法で完全分離してSPレイアウトを実装<br>・人間から見た見やすさ・美しさを最優先<br>・収まらないメニューはハンバーガーメニュー等で格納 |
| `/init-web-contents` | Web系プロジェクト初期設定 | ・`docker-compose up -d` で一発起動＆ローカルを汚さないコンテナ完結構成を構築<br>・デフォルト構成: **Vite (Frontend) + Go (Backend) + MariaDB (DB)**（※よりモダンな構成提案も可、フロントのみの場合はバックエンド省略可）<br>・DBの仮テーブルから `"hello im ready"` を取得してフロントエンドに表示するまでを初期ゴールとする<br>・ログイン画面がある場合はパスワード再設定機能を必須化、およびプロジェクト用 `README.md` を作成 |
| `/start-browser` | CDPモードChrome起動 (WSL2) | ・既存のChrome/Chromiumプロセスを終了し、`--remote-debugging-port=9222`（プロファイル: `~/.gemini/antigravity-browser-profile`）で再起動<br>・`http://127.0.0.1:9222/json/version` の応答確認まで自動実行 |

---

### 3. ライフサイクルHook (`hooks.json` / `hooks/safety-gate.py`)

`PreToolUse` イベント（`run_command` 実行直前）に `hooks/safety-gate.py` が実行され、コマンドの安全性を自動判定します。

#### 🚫 強制ブロック (`deny`)
以下の破滅的なコマンドパターンは、無条件で実行を拒否します。
- ルート (`/`)、ワイルドカード (`*`)、ホームディレクトリ (`~`, `$HOME`, `/home`) に対する `rm -rf`
- ファイルシステムのフォーマット (`mkfs.*`)
- ブロックデバイス (`/dev/sd*`, `/dev/nvme*`, `/dev/vd*`, `/dev/hd*`) への直接書き込み (`dd`)

#### ⚠️ 強制ユーザー確認 (`force_ask`)
以下の破壊的・不可逆なコマンドパターンを検知した場合、過去の許可キャッシュ（「常に許可」等）を無視して**必ずユーザーに実行確認プロンプトを表示**します。
- 再帰的な強制削除 (`rm -rf`, `rm --recursive`)
- Gitの強制プッシュ (`git push --force`, `-f`, `--force-with-lease`)
- コミット履歴・作業ツリーの強制破棄 (`git reset --hard`)
- 未追跡ファイルの強制削除 (`git clean -f`)
- Dockerリソースの一括削除 (`docker system/volume/container/image prune`)
- データベースやテーブルの削除クエリ (`DROP DATABASE`, `DROP TABLE`, `DROP SCHEMA`)

#### 🛡️ デフォルト判定
- サンドボックス内実行（`BypassSandbox: false`）: `allow`（自動許可）
- サンドボックス外実行（`BypassSandbox: true`）: `ask`（許可キャッシュを尊重しつつユーザー確認）

---

## 🔧 プラグインの有効化・無効化

Antigravity の設定ファイル（`~/.gemini/config.json`）または CLI からプラグインの有効・無効を切り替えられます。

```bash
# 有効化
agy plugin enable dddpga1-kit

# 無効化
agy plugin disable dddpga1-kit
```
