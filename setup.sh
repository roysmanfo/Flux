#!/usr/bin/env bash

# Flux setup script
# This script creates and configures the environment for flux
# by following these steps:
# 
# 1. check if venv exists, if not create it
# 2. activate venv
# 3. install requirements


SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
SCRIPT_NAME=$(echo $0 | tr "/" "\n" | tail -n 1)
SCRIPT_PATH=$(echo $SCRIPT_DIR/$SCRIPT_NAME)

MAIN="$SCRIPT_DIR/flux/main.py"
VENV="$SCRIPT_DIR/venv"
REQIREMENTS="$SCRIPT_DIR/linux-requirements.txt"

if [[ ! -d $VENV ]]; then
    
    echo creating virtual environment in \'$VENV\'
    mkdir $VENV -p 2>/dev/null
    python3 -m venv --prompt flux $VENV
    echo -e "# This file has been automatically created by flux\n" > "$VENV/.fluxenv"
    source $(echo $VENV/bin/activate)
    echo installing requirements
    python3 -m pip install -r $REQIREMENTS

else
    source $VENV/bin/activate

    if [[ $? != 0 ]]; then
        echo error in activation of \'$VENV\'
        exit 1
    fi
fi

if [[ $1 == "run" ]]; then
    cd flux
    python3 $MAIN
fi


