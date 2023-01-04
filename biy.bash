#!/usr/bin/env bash

# script params
#set -o nounset
set -o errexit
#set -o verbose

# setup general params
INIT_PWD=$(pwd)
SCRIPT_PATH=$(which $0)
SCRIPT_BASE=$(basename $0)
SCRIPT_DIR=$(cd $(dirname $0) && pwd)

echo "SCRIPT_DIR = ${SCRIPT_DIR}"

cd "${SCRIPT_DIR}"

poetry run biy-cli "$@"
