#!/bin/sh

has_tombi_targets() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    -name '*.toml' \
    -print -quit | grep -q .
}

if [ "$#" -eq 0 ] && ! has_tombi_targets; then
  printf '%s\n' 'No TOML files found; skipping tombi.'
  exit 0
fi

tombi lint --offline --error-on-warnings "$@" || exit $?
exec tombi format --offline --check "$@"
