#!/bin/sh

uses_baseline_gem_config() {
  # Keep in sync with hooks/rubocop.sh (separate config filenames).
  [ -f .erb_lint.yml ] && grep -Eq 'rubykatzen-baseline:' .erb_lint.yml 2>/dev/null
}

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

if [ ! -f Gemfile ]; then
  printf '%s\n' 'Gemfile not found. Add rubykatzen-baseline to the project Gemfile before running erb_lint.' >&2
  exit 1
fi

if ! uses_baseline_gem_config; then
  printf '%s\n' '.erb_lint.yml must inherit rubykatzen-baseline: config/erb_lint.yml before running erb_lint.' >&2
  exit 1
fi

if [ $# -eq 0 ]; then
  exec bundle exec erb_lint --lint-all
fi

exec bundle exec erb_lint "$@"
