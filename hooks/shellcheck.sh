#!/bin/sh
exec shellcheck --rcfile "$(dirname "$0")/../configs/shellcheck.rc" "$@"
