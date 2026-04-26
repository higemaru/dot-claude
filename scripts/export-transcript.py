#!/usr/bin/env python3
"""
Claude Code の会話 JSONL を Markdown に変換するスクリプト。
usage: python3 export-transcript.py <project_dir> [output_dir]
  project_dir: プロジェクトのルートディレクトリ（絶対パス）
  output_dir:  出力先ディレクトリ（省略時は project_dir/transcripts/）
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

def encode_project_path(path):
    """プロジェクトパスを ~/.claude/projects/ 以下のディレクトリ名に変換"""
    return path.replace("/", "-")

def extract_text(content):
    """content フィールドからテキストを取り出す"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                elif item.get("type") == "tool_use":
                    name = item.get("name", "tool")
                    parts.append(f"*[{name} を実行]*")
                elif item.get("type") == "tool_result":
                    pass  # ツール結果は省略
        return "\n".join(parts)
    return ""

def jsonl_to_markdown(jsonl_path):
    """JSONL ファイルを Markdown 文字列に変換"""
    messages = []
    first_ts = None

    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = entry.get("type")
            if entry_type not in ("user", "assistant"):
                continue

            msg = entry.get("message", {})
            content = msg.get("content", "")
            text = extract_text(content).strip()
            if not text:
                continue

            ts_raw = entry.get("timestamp") or msg.get("timestamp")
            ts_str = ""
            if ts_raw:
                try:
                    if isinstance(ts_raw, str):
                        dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00")).astimezone()
                    else:
                        dt = datetime.fromtimestamp(ts_raw / 1000, tz=timezone.utc).astimezone()
                    ts_str = dt.strftime("%H:%M")
                    if first_ts is None:
                        first_ts = dt
                except Exception:
                    pass

            messages.append((entry_type, ts_str, text))

    if not messages:
        return None, None

    date_str = first_ts.strftime("%Y-%m-%d") if first_ts else "unknown"

    lines = [f"# トランスクリプト {date_str}", ""]
    for role, ts, text in messages:
        if role == "user":
            header = f"## ユーザー {ts}".strip()
        else:
            header = f"## Claude {ts}".strip()
        lines.append(header)
        lines.append("")
        lines.append(text)
        lines.append("")

    return date_str, "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <project_dir> [output_dir]", file=sys.stderr)
        sys.exit(1)

    project_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) >= 3 else os.path.join(project_dir, "transcripts")
    os.makedirs(output_dir, exist_ok=True)

    claude_home = os.path.expanduser("~/.claude")
    encoded = encode_project_path(project_dir)
    project_data_dir = os.path.join(claude_home, "projects", encoded)

    if not os.path.isdir(project_data_dir):
        print(f"エラー: {project_data_dir} が見つかりません", file=sys.stderr)
        sys.exit(1)

    jsonl_files = sorted(
        f for f in os.listdir(project_data_dir) if f.endswith(".jsonl")
    )

    if not jsonl_files:
        print("JSONL ファイルが見つかりませんでした", file=sys.stderr)
        sys.exit(1)

    saved = []
    for fname in jsonl_files:
        jsonl_path = os.path.join(project_data_dir, fname)
        session_id = fname[:-6]
        date_str, md = jsonl_to_markdown(jsonl_path)
        if md is None:
            continue
        out_name = f"{date_str}_{session_id[:8]}.md"
        out_path = os.path.join(output_dir, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)
        saved.append(out_path)
        print(f"保存: {out_path}")

    print(f"\n{len(saved)} 件のトランスクリプトを {output_dir} に保存しました")

if __name__ == "__main__":
    main()
