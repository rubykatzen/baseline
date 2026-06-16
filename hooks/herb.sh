#!/bin/sh

has_erb_targets() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    \( -name '*.html.erb' -o -name '*.html+*.erb' \) \
    -print -quit | grep -q .
}

if ! has_erb_targets; then
  printf '%s\n' 'No HTML ERB files found; skipping herb.'
  exit 0
fi

if [ -f Gemfile ]; then
  bundle exec herb analyze .
else
  herb analyze .
fi
