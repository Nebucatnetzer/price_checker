#!/bin/bash
# Get the current working directory
SCRIPTPATH=$(dirname -- "$(readlink -e -- "$BASH_SOURCE")")

# add the bin directory to the path
PATH=$PATH:$SCRIPTPATH/bin/

# activate the virtual environment
source $SCRIPTPATH/bin/activate

# execute the main script
python3 $SCRIPTPATH/price_checker.py
exit 0
