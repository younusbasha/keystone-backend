@echo off
echo ======================================
echo GITHUB PUSH DIAGNOSTIC
echo ======================================

echo.
echo Checking key files:
if exist "app\api\v1\endpoints\auth.py" (echo ✅ auth.py exists) else (echo ❌ auth.py missing)
if exist "app\api\v1\endpoints\projects.py" (echo ✅ projects.py exists) else (echo ❌ projects.py missing)
if exist "app\api\v1\endpoints\requirements.py" (echo ✅ requirements.py exists) else (echo ❌ requirements.py missing)
if exist "TechSophy_Keystone_Complete_API_Collection.json" (echo ✅ Postman collection exists) else (echo ❌ Postman collection missing)
if exist "keystone.db" (echo ✅ keystone.db exists) else (echo ❌ keystone.db missing)

echo.
echo Git status:
git status

echo.
echo Recent commits:
git log --oneline -3

echo.
echo Remote configuration:
git remote -v

echo.
echo Current branch:
git branch

echo.
echo Staging all files...
git add -A

echo.
echo Checking staged files:
git status --porcelain

echo.
echo ======================================
echo DIAGNOSTIC COMPLETE
echo ======================================
pause
