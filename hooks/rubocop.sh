#!/bin/sh
BASELINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUBOCOP_CONFIG="$(mktemp)"

trap 'rm -f "$RUBOCOP_CONFIG"' EXIT

{
  printf '%s\n' 'inherit_from:'
  printf '  - %s\n' "$BASELINE_DIR/configs/rubocop.yml"

  for todo in .rubocop_todo*.yml; do
    [ -e "$todo" ] || continue
    printf '  - %s\n' "$PWD/$todo"
  done
} > "$RUBOCOP_CONFIG"

bundle exec rubocop --config "$RUBOCOP_CONFIG" "$@"
