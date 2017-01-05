#!/bin/bash
set -e

if [[ "$1" == "start" ]]; then
    service nginx start
  else
    set -- "$@"
    echo "args_other: $@"
    exec "$@"
fi
