#!/bin/bash
date=$(date "+%Y-%m-%d")
mkdir $date
echo "# "$date" 日报(曾伟)" >> $date"/007.md"
echo "---" >> $date"/007.md"
echo "## 1." >> $date"/007.md"
echo "## 2." >> $date"/007.md"
echo "## 3." >> $date"/007.md"
git add $date"/007.md"
git commit -m "feat: "$date"日常添加日报文件"
git push -u origin master
