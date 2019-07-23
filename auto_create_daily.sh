#!/bin/bash
git stash
git pull
date=$(date "+%Y-%m-%d")
mkdir $date
echo "# "$date" 日报(曾伟)" >> $date"/README.md"
echo "---" >> $date"/README.md"
echo "## 1." >> $date"/README.md"
echo "## 2." >> $date"/README.md"
echo "## 3." >> $date"/README.md"
git add $date"/README.md"
git commit -m "feat: "$date"日常添加日报文件"
git push -u origin master
