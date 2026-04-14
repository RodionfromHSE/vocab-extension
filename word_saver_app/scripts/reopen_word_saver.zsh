#!/bin/zsh

APPLICATION_NAME="word-saver"

killall "$APPLICATION_NAME" 2>/dev/null

# wait for the process to actually die before reopening
while pgrep -x "$APPLICATION_NAME" > /dev/null 2>&1; do
    sleep 0.2
done

open -a "$APPLICATION_NAME"
echo "Word Saver reopened"
