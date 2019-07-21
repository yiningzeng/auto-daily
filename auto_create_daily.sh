#!/bin/bash
date=$(date "+%Y-%m-%d")
mkdir $date
echo "# "$date" 日报(曾伟)" >> $date"/007.txt"
echo "---" >> $date"/007.txt"
echo "## 1." >> $date"/007.txt"
echo "## 2." >> $date"/007.txt"
echo "## 3." >> $date"/007.txt"
git add $date"/007.txt"
git commit -m "feat: "$date"日常添加日报文件"
git push -u origin master
