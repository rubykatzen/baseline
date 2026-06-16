#!/bin/sh

has_herb_targets() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    \( -name '*.html.erb' -o -name '*.html+*.erb' -o -name '*.turbo_stream.erb' \
       -o -name '*.herb' -o -name '*.html.herb' -o -name '*.rhtml' \) \
    -print -quit | grep -q .
}

if ! has_herb_targets; then
  printf '%s\n' 'No ERB/Herb files found; skipping herb.'
  exit 0
fi

if [ -f Gemfile ]; then
  bundle exec herb analyze .
else
  herb analyze .
fi
