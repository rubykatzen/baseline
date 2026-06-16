#!/bin/sh

has_js_targets() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    \( -name '*.js' -o -name '*.jsx' -o -name '*.mjs' -o -name '*.cjs' \) \
    -print -quit | grep -q .
}

if ! has_js_targets; then
  printf '%s\n' 'No JavaScript files found; skipping standard.'
  exit 0
fi

npx standard
