import os
import interactions

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = interactions.Client(token=TOKEN)

@bot.command(name='ping', description="Send the ping of the bot.")
async def ping(ctx: interactions.CommandContext):
    await ctx.send(f"Pong! {bot.latency.__round__(1)} ms.")

bot.start()