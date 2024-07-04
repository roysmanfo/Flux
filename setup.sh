#!/usr/bin/env bash

# Flux setup script
# This script creates and configures the environment for flux
# by following these steps:
# 
# 1. check if venv exists, if not create it
# 2. activate venv
# 3. install requirements

DEVNULL="/dev/null"
SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> $DEVNULL && pwd)
SCRIPT_NAME=$(echo $0 | tr "/" "\n" | tail -n 1)
SCRIPT_PATH=$(echo $SCRIPT_DIR/$SCRIPT_NAME)

MAIN="$SCRIPT_DIR/flux/main.py"
VENV="$SCRIPT_DIR/.venv"
REQIREMENTS="$SCRIPT_DIR/linux-requirements.txt"


createVenv() {
    echo creating virtual environment in \'$VENV\'
    mkdir $VENV -p 2>$DEVNULL
    python3 -m venv --prompt flux $VENV
    echo -e "# This file has been automatically created by flux\n" > "$VENV/.fluxenv"
    source $(echo $VENV/bin/activate)
    echo installing requirements
    python3 -m pip install -r $REQIREMENTS

    exit $?
}


if [[ ! -d $VENV ]]; then
    createVenv
else
    source $VENV/bin/activate 2> $DEVNULL

    if [[ $? != 0 ]]; then
        echo Err: error in activation of \'$VENV\'
        echo -n "recreate environment (y/n)?: "
        read res
        
        if [[ $res != "y" ]]; then
            echo $res
            exit 1
        fi 

        # 'rm -rf' is often seen as a danger
        # but in this case the path to delete
        # is well defined and symlinks are not followed
        echo removing \'$VENV\'
        rm -rf $VENV
        createVenv
    fi
fi

if [[ $1 == "run" ]]; then
    cd flux
    python3 $MAIN
fi


