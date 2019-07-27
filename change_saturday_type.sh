#!/bin/bash
echo -n $1 |tee is_holiday.md
git add "is_holiday.md"
git commit -m "feat: 更改下周六的工作类型"
git push -u origin master