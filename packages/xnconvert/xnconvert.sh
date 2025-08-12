#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
export LD_LIBRARY_PATH="$SCRIPT_DIR/lib"
export QT_PLUGIN_PATH="$SCRIPT_DIR/lib"
exec "$SCRIPT_DIR/XnConvert" "$@"
