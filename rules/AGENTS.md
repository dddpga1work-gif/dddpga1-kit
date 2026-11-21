- やりとりやユーザーに関する表示は日本語で行うこと
- 全てのプロジェクトは他者に渡すことも想定し、docker-compose up -d等で一発で起動できるようにし、そのコンテナ内で全て完結し、localを汚すことは一切ないものとする
- 不明点は必ずユーザーに説明をした後、確認を取ってから実行に移す
- エラー内容を渡されたり修正を依頼された場合は、対応の後に全体を精査しなおし、修正によって更なるエラーや不整合、仕様の破壊等が起こらないか確認を必ずして報告する
- 知識が古いことが多々あり、決めつけて回答することが多々確認できている。例として、google cloud vertex aiでつかるgeminiのモデルの最新は1.5 proか2.1 flashだと毎回回答している。が、実際は2026/08/02時点で3.1 proか3.5 flash及び3.6 flashであるという事実がある。1.5や2.1は既にモデルとして使えなくなっているのにも関わらずだ。そのため、必ずwebや公式ドキュメント最新版での調査をしないと回答できないものとする。そして調査は必須とする
- 対処療法は絶対的に禁止。必ず根源治療を最新の仕様や指示に合わせて行うこと
- 作成するものはモダンであり、例えばjQuery等の古いものの利用は一切禁止とする

- 通常コマンドの実行時は WaitMsBeforeAsync を常に最大値（10000ms）にし、安易にバックグラウンドタスク化させないこと。またバックグラウンドタスクを放置してターンを終了することを禁止する。

## Browser Subagent (WSL2 Environment)
Before using the `browser_subagent` tool in a WSL2 environment, you MUST first run the `/start-browser` workflow to launch Chrome/Chromium in CDP mode. Without this step, browser_subagent will fail with "CDP port not responsive" errors.
Global Workflow: `/start-browser`
