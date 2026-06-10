#!/bin/sh
exec yamllint -c "$(dirname "$0")/../yamllint_dupmachine/config.yml" "$@"
