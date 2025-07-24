@echo off
set MESSAGE=%1

git add .
git commit -m "%MESSAGE%"
git push -u https://github.com/biceps-yeon/LPPL-CI-of-KOSPI-S-P500-TESLA.git master