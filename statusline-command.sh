#!/bin/bash
# Claude Code ステータスライン: コンテキスト使用率プログレスバー + モデル名

input=$(cat)

model=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

if [ -z "$used" ]; then
  printf "%s | Context: --" "$model"
  exit 0
fi

used_int=$(printf "%.0f" "$used")

# プログレスバー生成 (20マス)
bar_total=20
bar_filled=$(( used_int * bar_total / 100 ))
[ $bar_filled -gt $bar_total ] && bar_filled=$bar_total
bar_empty=$(( bar_total - bar_filled ))

bar=""
for i in $(seq 1 $bar_filled); do bar="${bar}█"; done
for i in $(seq 1 $bar_empty); do bar="${bar}░"; done

# 色: 0-60% 緑, 60-80% 黄, 80%以上 赤
if [ "$used_int" -ge 80 ]; then
  color="\033[31m"   # 赤
elif [ "$used_int" -ge 60 ]; then
  color="\033[33m"   # 黄
else
  color="\033[32m"   # 緑
fi
reset="\033[0m"

printf "%s | Context: ${color}[%s] %d%%${reset}" "$model" "$bar" "$used_int"
