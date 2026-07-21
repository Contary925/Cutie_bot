from datetime import datetime, timezone
async def ping(message):
    ping_duration_seconds = (datetime.now(timezone.utc) - message.created_at).total_seconds()
    await message.channel.send(f"Pong! {max(0, int(ping_duration_seconds*1000))} ms")