robocopy .\website ..\terrawhisper\ /E
cd ..
cd terrawhisper
git add .
git commit -m "'"
git push --force
cd ..
cd terrawhisper-compiler