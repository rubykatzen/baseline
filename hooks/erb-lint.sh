#!/bin/sh
BASELINE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

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
BEFORE_DIFF="$(mktemp)"
AFTER_DIFF="$(mktemp)"
trap 'rm -f "$RUBOCOP_CONFIG" "$ERB_LINT_CONFIG" "$BEFORE_DIFF" "$AFTER_DIFF"' EXIT

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

# Autocorrect pass — local only, skipped in CI so style drift fails the build
if [ -z "$CI" ]; then
  git diff --name-only | sort > "$BEFORE_DIFF"

  if [ $# -gt 0 ]; then
    if [ -f Gemfile ]; then
      bundle exec erb_lint --autocorrect --config "$ERB_LINT_CONFIG" "$@" || true
    else
      erb_lint --autocorrect --config "$ERB_LINT_CONFIG" "$@" || true
    fi
  else
    if [ -f Gemfile ]; then
      erb_files -print0 | xargs -0 bundle exec erb_lint --autocorrect --config "$ERB_LINT_CONFIG" || true
    else
      erb_files -print0 | xargs -0 erb_lint --autocorrect --config "$ERB_LINT_CONFIG" || true
    fi
  fi

  git diff --name-only | sort > "$AFTER_DIFF"
  autocorrected=$(comm -13 "$BEFORE_DIFF" "$AFTER_DIFF")

  if [ -n "$autocorrected" ]; then
    printf 'erb-lint: autocorrected:\n'
    printf '%s\n' "$autocorrected" | while IFS= read -r f; do
      printf '  %s\n' "$f"
      git add -- "$f"
    done
  fi
fi

# Lint pass
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
