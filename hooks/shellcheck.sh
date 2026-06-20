#!/bin/sh

config="$(dirname "$0")/../config/shellcheck.rc"

shell_files() {
  find . \
    \( -path ./.git -o -path ./vendor -o -path ./node_modules \) -prune -o \
    -type f \
    -name '*.sh' \
    "$@"
}

if [ $# -eq 0 ]; then
  if ! shell_files -print -quit | grep -q .; then
    printf '%s\n' 'No shell files found; skipping shellcheck.'
    exit 0
  fi
  shell_files -exec shellcheck --rcfile "$config" {} +
  exit $?
fi

exec shellcheck --rcfile "$config" "$@"
