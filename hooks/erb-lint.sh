#!/bin/sh
BASELINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# When called with file args (pre-commit), use those.
# Otherwise find all ERB files, explicitly excluding vendor/node_modules.
if [ $# -gt 0 ]; then
  ERB_FILES="$*"
else
  ERB_FILES=$(find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    \( -name '*.html.erb' -o -name '*.html+*.erb' \) \
    -print)
fi

if [ -z "$ERB_FILES" ]; then
  printf '%s\n' 'No HTML ERB files found; skipping erb_lint.'
  exit 0
fi

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
  # shellcheck disable=SC2086
  bundle exec erb_lint --config "$ERB_LINT_CONFIG" $ERB_FILES
else
  # shellcheck disable=SC2086
  erb_lint --config "$ERB_LINT_CONFIG" $ERB_FILES
fi
