#!/bin/sh

has_shellcheck_targets() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    -name '*.sh' \
    -print -quit | grep -q .
}

if [ $# -eq 0 ] && ! has_shellcheck_targets; then
  printf '%s\n' 'No shell files found; skipping shellcheck.'
  exit 0
fi

exec shellcheck --rcfile "$(dirname "$0")/../configs/shellcheck.rc" "$@"
