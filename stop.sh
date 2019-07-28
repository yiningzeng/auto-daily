#!/bin/bash
kill -9 `cat pid.txt`
ps -ef |grep daily.py
rm pid.txt
echo "success"
