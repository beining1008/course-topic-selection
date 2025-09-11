@echo off
echo 正在上传代码到GitHub...
echo.

REM GitHub仓库URL
set REPO_URL=https://github.com/beining1008/course-topic-selection.git

echo 添加远程仓库...
git remote add origin %REPO_URL%

echo 重命名分支为main...
git branch -M main

echo 推送代码到GitHub...
git push -u origin main

echo.
echo 上传完成！
echo 现在您可以访问 https://share.streamlit.io 来部署应用了
pause
