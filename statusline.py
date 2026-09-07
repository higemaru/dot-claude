#!/usr/bin/env python3
# Claude Code ステータスライン: コンテキスト使用率プログレスバー + モデル名
import sys
import json

try:
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)
    data = json.loads(raw)

    model = data.get("model", {})
    if isinstance(model, dict):
        model_name = model.get("display_name") or model.get("id") or "Unknown"
    elif isinstance(model, str):
        model_name = model
    else:
        model_name = "Unknown"

    cw = data.get("context_window", {})
    if not isinstance(cw, dict):
        cw = {}

    used = cw.get("used_percentage")

    if used is None or used == "":
        print(f"{model_name} | Context: --", end="")
        sys.exit(0)

    try:
        used_int = round(float(used))
    except (ValueError, TypeError):
        print(f"{model_name} | Context: --", end="")
        sys.exit(0)

    # プログレスバー生成 (20マス)
    bar_total = 20
    bar_filled = int(used_int * bar_total / 100)
    if bar_filled > bar_total:
        bar_filled = bar_total
    elif bar_filled < 0:
        bar_filled = 0
    bar_empty = bar_total - bar_filled

    bar = "█" * bar_filled + "░" * bar_empty

    # 色: 0-60% 緑, 60-80% 黄, 80%以上 赤
    if used_int >= 80:
        color = "\033[31m"   # 赤
    elif used_int >= 60:
        color = "\033[33m"   # 黄
    else:
        color = "\033[32m"   # 緑
    reset = "\033[0m"

    print(f"{model_name} | Context: {color}[{bar}] {used_int}%{reset}", end="")
except Exception:
    pass
