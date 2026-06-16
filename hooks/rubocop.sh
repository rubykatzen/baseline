#!/bin/sh
BASELINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

ruby_files() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    \( -name '*.rb' -o -name '*.rake' -o -name '*.gemspec' -o -name 'Gemfile' -o -name 'Rakefile' -o -name 'config.ru' \) \
    "$@"
}

if [ $# -eq 0 ] && ! ruby_files -print -quit | grep -q .; then
  printf '%s\n' 'No Ruby files found; skipping rubocop.'
  exit 0
fi

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

if [ $# -gt 0 ]; then
  if [ -f Gemfile ]; then
    bundle exec rubocop --config "$RUBOCOP_CONFIG" "$@"
  else
    rubocop --config "$RUBOCOP_CONFIG" "$@"
  fi
else
  if [ -f Gemfile ]; then
    ruby_files -print0 | xargs -0 bundle exec rubocop --config "$RUBOCOP_CONFIG"
  else
    ruby_files -print0 | xargs -0 rubocop --config "$RUBOCOP_CONFIG"
  fi
fi
