#!/bin/sh

uses_baseline_gem_config() {
  # Keep in sync with hooks/erb-lint.sh (separate config filenames).
  [ -f .rubocop.yml ] && grep -Eq 'rubykatzen-baseline:' .rubocop.yml 2>/dev/null
}

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

if [ ! -f Gemfile ]; then
  printf '%s\n' 'Gemfile not found. Add rubykatzen-baseline to the project Gemfile before running rubocop.' >&2
  exit 1
fi

if ! uses_baseline_gem_config; then
  printf '%s\n' '.rubocop.yml must inherit rubykatzen-baseline: config/rubocop.yml before running rubocop.' >&2
  exit 1
fi

exec bundle exec rubocop "$@"
