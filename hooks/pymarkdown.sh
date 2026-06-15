#!/bin/sh

has_pymarkdown_targets() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    \( -name '*.md' -o -name '*.markdown' \) \
    -print -quit | grep -q .
}

if ! has_pymarkdown_targets; then
  printf '%s\n' 'No Markdown files found; skipping pymarkdown.'
  exit 0
fi

exec pymarkdown --config "$(dirname "$0")/../configs/pymarkdown.json" scan "$@"
