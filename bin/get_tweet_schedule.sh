#!/bin/bash

JOBS="$(atq)"

if [ -z "$JOBS" ]; then
    exit
fi

while read -r line
do
    QUEUE="$(echo "$line" | awk '{printf $7}')";
    if [ $QUEUE == "d" ]; then
        echo "$(echo "$line" | awk '{print $6, $3, $4, $5, $1}')"
    fi
done < <(printf '%s\n' "$JOBS")

