@echo off
echo Setting up Git configuration...
git config user.name "Younus Basha"
git config user.email "skybash@yahoo.com"

echo Checking git status...
git status

echo Adding all files...
git add .

echo Committing changes...
git commit -m "Complete comprehensive API implementation with 160+ endpoints - All CRUD operations, AI features, real-time capabilities for TechSophy Keystone SDLC platform"

echo Removing existing remote...
git remote remove origin 2>nul

echo Adding GitHub remote with token...
git remote add origin https://younusbasha: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@github.com/younusbasha/keystone-backend.git

echo Pushing to GitHub master branch...
git push -u origin master

echo Verifying push...
git log --oneline -3

echo Done! Check GitHub repository for changes.
pause
