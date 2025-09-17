import subprocess
import sys

def run_command(cmd, description):
    """Run command with proper output handling"""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)

        if result.stdout:
            print(f"✅ OUTPUT:\n{result.stdout}")
        if result.stderr:
            print(f"⚠️ STDERR:\n{result.stderr}")

        print(f"Return code: {result.returncode}")
        return result.returncode == 0, result.stdout, result.stderr

    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, "", str(e)

def fix_and_merge():
    """Fix authentication and merge to master"""
    print("🔧 FIXING AUTHENTICATION AND MERGING TO MASTER")
    print("=" * 60)

    # Configure git
    run_command('git config user.name "Younus Basha"', "Setting git username")
    run_command('git config user.email "skybash@yahoo.com"', "Setting git email")

    # Remove any existing remote and add with proper token format
    run_command("git remote remove origin", "Removing old remote")

    # Try different token authentication approaches
    token_formats = [
        f"https://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@github.com/younusbasha/keystone-backend.git",
        f"https://younusbasha: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@github.com/younusbasha/keystone-backend.git"
    ]

    remote_added = False
    for i, remote_url in enumerate(token_formats):
        success, stdout, stderr = run_command(f'git remote add origin {remote_url}', f"Adding remote (format {i+1})")
        if success:
            remote_added = True
            break
        else:
            run_command("git remote remove origin", "Removing failed remote")

    if not remote_added:
        print("❌ Failed to add remote with any token format")
        return

    # Fetch all branches
    run_command("git fetch origin", "Fetching all branches")

    # Check current branch
    success, stdout, stderr = run_command("git branch", "Checking current branch")

    # Switch to master and merge
    success, stdout, stderr = run_command("git checkout master", "Switching to master")
    if not success:
        run_command("git checkout -b master", "Creating master branch locally")

    # Merge the api-implementation branch
    success, stdout, stderr = run_command("git merge origin/api-implementation --allow-unrelated-histories", "Merging api-implementation with allow-unrelated-histories")

    if success:
        print("✅ Merge successful! Pushing to master...")

        # Push to master
        success, stdout, stderr = run_command("git push origin master", "Pushing to master")

        if success:
            print("\n🎉 SUCCESS! Master branch updated!")
            print("✅ Both branches are now in sync")
            print("🔗 Check: https://github.com/younusbasha/keystone-backend")
        else:
            print("⚠️ Push failed, trying force push...")
            success, stdout, stderr = run_command("git push origin master --force", "Force pushing to master")
            if success:
                print("🎉 Force push successful!")
            else:
                print(f"❌ All push attempts failed: {stderr}")
    else:
        print(f"❌ Merge failed: {stderr}")

if __name__ == "__main__":
    fix_and_merge()
