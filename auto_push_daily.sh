#!/bin/bash
date=$(date "+%Y-%m-%d")
git add $date"/README.md"
git commit -m "feat: "$date"日常更新日报文件"
git push -u origin master