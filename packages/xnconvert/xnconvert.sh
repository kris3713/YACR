#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
export LD_LIBRARY_PATH="$SCRIPT_DIR/lib:$LD_LIBRARY_PATH"
export QT_PLUGIN_PATH="$SCRIPT_DIR/lib:$QT_PLUGIN_PATH"
exec "$SCRIPT_DIR/XnConvert" "$@"
