#!/bin/sh

has_ruff_targets() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    \( -name '*.py' -o -name '*.pyi' \) \
    -print -quit | grep -q .
}

if ! has_ruff_targets; then
  printf '%s\n' 'No Python files found; skipping ruff.'
  exit 0
fi

exec ruff check --config "$(dirname "$0")/../configs/ruff.toml" "$@"
