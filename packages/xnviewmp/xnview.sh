#!/usr/bin/env bash

dirname=$(dirname "$(readlink -e "$0")")
export LD_LIBRARY_PATH="$dirname/lib:$dirname/Plugins:$LD_LIBRARY_PATH"
export QT_PLUGIN_PATH="$dirname/lib:$QT_PLUGIN_PATH"
"$dirname/XnView" "$@"
