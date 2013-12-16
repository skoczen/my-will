#!/bin/sh

`find . -name "run_will.py"` &
PID=$!
sleep 10
RUNNING=`ps a | grep run_will | grep -v grep | wc -l`
if [ ${RUNNING} -gt 0 ]; then
    kill $PID
    ps a | grep run_will | grep -v grep | awk '{print $1}' | xargs kill -9
    exit 0;
else
    exit 1;
fi