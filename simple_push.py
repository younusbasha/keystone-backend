import subprocess
import sys

# Just run the git commands directly and exit with status
try:
    # Configure git
    subprocess.run('git config user.name "Younus Basha"', shell=True, check=True)
    subprocess.run('git config user.email "skybash@yahoo.com"', shell=True, check=True)

    # Add all files
    subprocess.run("git add -A", shell=True, check=True)

    # Commit
    subprocess.run('git commit -m "Complete comprehensive API - 160+ endpoints"', shell=True)

    # Set remote with token
    subprocess.run("git remote remove origin", shell=True)
    subprocess.run("git remote add origin https://younusbasha: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@github.com/younusbasha/keystone-backend.git", shell=True, check=True)

    # Create branch and push
    subprocess.run("git checkout -b api-implementation", shell=True, check=True)
    subprocess.run("git push -u origin api-implementation", shell=True, check=True)

    print("SUCCESS: Pushed to GitHub!")

except subprocess.CalledProcessError as e:
    print(f"ERROR: {e}")
    sys.exit(1)
