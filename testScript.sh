#!/bin/bash

OD="succc"

for arg in "$@"
do
    if [[ "$arg" == "--oldData" ]] && [[ "$OD" == "succc" ]]
    then
        echo "Training will use old data"
        OD="TRUE"
    fi
done
