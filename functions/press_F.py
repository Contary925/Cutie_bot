import asyncio
import time

async def press_F(client, message, content):
    F_message = await message.channel.send(f"Press F to pay respects to **{content}**.")
    await F_message.add_reaction('🇫')
    def check(reaction, user):
        return (
            reaction.message.id == F_message.id
            and str(reaction.emoji) == '🇫'
        )
    count = 0
    end_time = time.time() + 15.0
    while True:
        remaining_time = end_time - time.time()
        try:
            reaction, reactor = await client.wait_for(
                'reaction_add',
                timeout=remaining_time,
                check=check
            )
            await message.channel.send(f'{reactor.display_name} has paid their respects.')
            count += 1
        except asyncio.TimeoutError:
            match count:
                case 0:
                    await message.channel.send(f'Nobody paid their respects to **{content}**. What a shame...')
                case 1:
                    await message.channel.send(f'One user has paid their respects to **{content}**.')
                case _:
                    await message.channel.send(f'{count} users have paid their respects to **{content}**.')
            break