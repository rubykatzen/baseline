#!/bin/sh
BASELINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUBOCOP_CONFIG="$(mktemp)"
ERB_LINT_CONFIG="$(mktemp)"

trap 'rm -f "$RUBOCOP_CONFIG" "$ERB_LINT_CONFIG"' EXIT

{
  printf '%s\n' 'inherit_from:'
  printf '  - %s\n' "$BASELINE_DIR/configs/rubocop.yml"

  for todo in .rubocop_todo*.yml; do
    [ -e "$todo" ] || continue
    printf '  - %s\n' "$PWD/$todo"
  done

  for todo in .erb_lint_todo*.yml; do
    [ -e "$todo" ] || continue
    printf '  - %s\n' "$PWD/$todo"
  done

  printf '%s\n' 'Layout/TrailingEmptyLines:'
  printf '%s\n' '  Enabled: false'
  printf '%s\n' 'Layout/InitialIndentation:'
  printf '%s\n' '  Enabled: false'
  printf '%s\n' 'Lint/UselessAssignment:'
  printf '%s\n' '  Enabled: false'
} > "$RUBOCOP_CONFIG"

{
  printf '%s\n' 'inherit_from:'
  printf '  - %s\n' "$BASELINE_DIR/configs/erb-lint.yml"

  printf '%s\n' 'linters:'
  printf '%s\n' '  Rubocop:'
  printf '    config_file_path: %s\n' "$RUBOCOP_CONFIG"
} > "$ERB_LINT_CONFIG"
if [ -f Gemfile ]; then
  bundle exec erb_lint --config "$ERB_LINT_CONFIG" "$@"
else
  erb_lint --config "$ERB_LINT_CONFIG" "$@"
fi
