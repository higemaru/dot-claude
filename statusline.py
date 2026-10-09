#!/usr/bin/env python3
"""Claude Code statusline: model | context | 5h session | weekly limit."""
import json
import sys
import time

RESET = "\033[0m"
DIM = "\033[2m"


def color(pct):
    if pct >= 80:
        return "\033[31m"
    if pct >= 60:
        return "\033[33m"
    return "\033[32m"


def bar(pct, width=10):
    filled = max(0, min(width, int(pct / 100 * width)))
    return "█" * filled + "░" * (width - filled)


def remaining(resets_at):
    """resets_at: epoch seconds -> '4h49m' / '2d3h'."""
    try:
        secs = int(float(resets_at) - time.time())
    except (TypeError, ValueError):
        return ""
    if secs <= 0:
        return ""
    d, rem = divmod(secs, 86400)
    h, rem = divmod(rem, 3600)
    m = rem // 60
    if d:
        return f"{d}d{h}h"
    if h:
        return f"{h}h{m:02d}m"
    return f"{m}m"


def segment(label, info):
    if not isinstance(info, dict) or info.get("used_percentage") is None:
        return f"{label} --"
    try:
        pct = round(float(info["used_percentage"]))
    except (TypeError, ValueError):
        return f"{label} ?"
    c = color(pct)
    b = f"{bar(pct)} "
    reset = remaining(info.get("resets_at"))
    tail = f"{DIM} ↻{reset}{RESET}" if reset else ""
    return f"{label} {c}{b}{pct}%{RESET}{tail}"


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    if not isinstance(data, dict):
        return

    model = data.get("model") or {}
    name = (model.get("display_name") or model.get("id") or "Unknown") if isinstance(model, dict) else str(model)

    parts = [name, segment("Ctx", data.get("context_window"))]

    limits = data.get("rate_limits")
    if isinstance(limits, dict) and limits:
        parts.append(segment("5h", limits.get("five_hour")))
        parts.append(segment("7d", limits.get("seven_day")))

    sys.stdout.write(" | ".join(parts))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
