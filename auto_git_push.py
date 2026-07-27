import subprocess
async def sync_to_github(message):
    try:
        await message.channel.send("Uploading to GitHub...")
        subprocess.run(["git", "add", "."], check=True)
        commit_message = "Auto-commit on bot shutdown"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True, stdout=subprocess.DEVNULL)
        await message.channel.send("Uploaded successfully!")
        return True
    except subprocess.CalledProcessError as e:
        await message.channel.send(f"Git sync failed with error: {e}")
        return False
