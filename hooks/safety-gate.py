#!/usr/bin/env python3
import json
import re
import sys

# 絶対ブロック（deny）する破滅的コマンドパターン
DENY_PATTERNS = [
    (r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\s+(/|\*|~|\$HOME|/home\b)", "ルートまたはホームディレクトリの強制削除は禁止されています。"),
    (r"\bmkfs(\.[a-z0-9]+)?\b", "ファイルシステムのフォーマットコマンドは禁止されています。"),
    (r"\bdd\s+.*of=/dev/(sd|nvme|vd|hd)", "ブロックデバイスへの直接書き込みは禁止されています。"),
]

# 常にユーザーへ確認を求める（force_ask）危険コマンドパターン
ASK_PATTERNS = [
    (r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r|--recursive)\b", "再帰的な強制削除 (rm -rf) が含まれています。"),
    (r"\bgit\s+push\s+.*(--force|-f|--force-with-lease)\b", "強制プッシュ (git push --force) が含まれています。"),
    (r"\bgit\s+reset\s+--hard\b", "コミット履歴・作業ツリーを破棄する git reset --hard が含まれています。"),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "未追跡ファイルを削除する git clean -f が含まれています。"),
    (r"\bdocker\s+(system|volume|container|image)\s+prune\b", "Dockerリソースの一括削除 (prune) が含まれています。"),
    (r"(?i)\bdrop\s+(database|table|schema)\b", "データベース／テーブルの削除クエリ (DROP) が含まれています。"),
]


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print(json.dumps({"decision": "ask"}))
        return

    tool_call = payload.get("toolCall") or {}
    args = tool_call.get("args") or {}
    cmd = args.get("CommandLine") or ""
    bypass_sandbox = bool(args.get("BypassSandbox"))

    for pattern, reason in DENY_PATTERNS:
        if re.search(pattern, cmd):
            print(json.dumps({
                "decision": "deny",
                "reason": f"[dddpga1-kit Safety Gate] {reason} (Command: {cmd})"
            }, ensure_ascii=False))
            return

    for pattern, reason in ASK_PATTERNS:
        if re.search(pattern, cmd):
            print(json.dumps({
                "decision": "force_ask",
                "reason": f"[dddpga1-kit Safety Gate] {reason} 実行してよろしいですか？"
            }, ensure_ascii=False))
            return

    # サンドボックス外実行（BypassSandbox: true）はキャッシュを尊重しつつ確認（ask）、サンドボックス内は許可（allow）
    default_decision = "ask" if bypass_sandbox else "allow"
    print(json.dumps({"decision": default_decision}))


if __name__ == "__main__":
    main()
