import subprocess
def pull_from_github():
    try:
        print("Starting to sync with GitHub...")
        subprocess.run(["git", "pull", "origin", "main"], check=True, stdout=subprocess.DEVNULL)
        print("Updated successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git sync failed with error: {e}")
        return False