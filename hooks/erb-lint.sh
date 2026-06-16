#!/bin/sh
BASELINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

uses_baseline_gem_config() {
  [ -f .erb_lint.yml ] && grep -Eq '^[[:space:]]*baseline:' .erb_lint.yml 2>/dev/null
}

if uses_baseline_gem_config && [ -f Gemfile ]; then
  if [ $# -eq 0 ]; then
    exec bundle exec erb_lint --lint-all "$@"
  fi

  exec bundle exec erb_lint "$@"
fi

erb_files() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    \( -name '*.html.erb' -o -name '*.html+*.erb' \) \
    "$@"
}

if [ $# -eq 0 ] && ! erb_files -print -quit | grep -q .; then
  printf '%s\n' 'No HTML ERB files found; skipping erb_lint.'
  exit 0
fi

RUBOCOP_CONFIG="$(mktemp)"
ERB_LINT_CONFIG="$(mktemp)"
trap 'rm -f "$RUBOCOP_CONFIG" "$ERB_LINT_CONFIG"' EXIT

{
  printf '%s\n' 'inherit_from:'
  printf '  - %s\n' "$BASELINE_DIR/config/rubocop.yml"

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
  printf '  - %s\n' "$BASELINE_DIR/config/erb_lint.yml"

  printf '%s\n' 'linters:'
  printf '%s\n' '  Rubocop:'
  printf '    config_file_path: %s\n' "$RUBOCOP_CONFIG"
} > "$ERB_LINT_CONFIG"

if [ $# -gt 0 ]; then
  if [ -f Gemfile ]; then
    bundle exec erb_lint --config "$ERB_LINT_CONFIG" "$@"
  else
    erb_lint --config "$ERB_LINT_CONFIG" "$@"
  fi
else
  if [ -f Gemfile ]; then
    erb_files -print0 | xargs -0 bundle exec erb_lint --config "$ERB_LINT_CONFIG"
  else
    erb_files -print0 | xargs -0 erb_lint --config "$ERB_LINT_CONFIG"
  fi
fi
