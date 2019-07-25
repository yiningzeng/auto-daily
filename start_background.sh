#!/bin/bash
nohup python daily.py $1> wechat.log 2>&1 &
pid=$!
echo "pid $pid running"
echo $pid > pid.txt
