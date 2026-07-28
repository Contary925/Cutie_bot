import subprocess
from shared.ID import OWNER_ID
from functions.check_owner import check_owner
async def sync_to_github(message):
    if await check_owner() :
        try:
            await message.channel.send("Uploading to GitHub...")
            subprocess.run(["git", "add", "."], check=True)
            commit_message = "Auto-commit on bot shutdown"
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True, stdout=subprocess.DEVNULL)
            await message.channel.send("Uploaded successfully!")
            return True
        except subprocess.CalledProcessError as e:
            await message.channel.send(f"Git sync failed with error: {e}")
            return False
