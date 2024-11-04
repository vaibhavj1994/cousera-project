#!/bin/bash

# This script is to temporarily change the dynamic linker variable to help it locate the libmysqlclient.24.lib library
# since i'm getting errors when running migrations

# ./helper_script.sh python3 manage.py migrate

# Store the current DYLD_LIBRARY_PATH
ORIGINAL_DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH

# Set the DYLD_LIBRARY_PATH to include MySQL library path
export DYLD_LIBRARY_PATH="/usr/local/mysql/lib:$DYLD_LIBRARY_PATH"

# Execute the given command
"$@"

# Restore the original DYLD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$ORIGINAL_DYLD_LIBRARY_PATH