#!/usr/bin/env bash

# Flux setup script
# This script creates and configures the environment for flux
# by following these steps:
# 
# 1. check if venv exists, if not create it
# 2. activate venv
# 3. install requirements

SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
SCRIPT_NAME=$(basename "$0")
SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT_NAME"

MAIN="$SCRIPT_DIR/flux/main.py"
VENV="$SCRIPT_DIR/venv"
REQUIREMENTS="$SCRIPT_DIR/linux-requirements.txt"

if [[ ! -d $VENV ]]; then
    echo creating virtual environment in \'$VENV\'
    python3 -m venv --prompt flux "$VENV"
    echo -e "# This file has been automatically created by flux\n" > "$VENV/.fluxenv"
    source "$VENV/bin/activate"
    echo installing requirements
    python3 -m pip install -r "$REQUIREMENTS"
else 
    source "$VENV/bin/activate" 2>/dev/null
    
    if [[ $? != 0 ]]; then
        # ? maybe this is windows
        source "$VENV/Scripts/activate" 2>/dev/null

        if [[ $? != 0 ]]; then
            echo error in activation of \'$VENV\'
            exit 1
        fi
    fi
fi

if [[ $1 == "run" ]]; then
    cd flux
    python3 "$MAIN"
fi
