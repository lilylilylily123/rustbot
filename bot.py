import os
import interactions

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = interactions.Client(token=TOKEN)
@bot.event()
async def on_ready():
    print(f"Connected.")
@bot.event()
async def on_guild_member_add(ctx: interactions.GuildMember):
    await ctx.send(f"Welcome!")
@bot.command(name='ping', description="Send the ping of the bot.")
async def ping(ctx: interactions.CommandContext):
    await ctx.send(f"Pong! {bot.latency.__round__(0)} ms.")

bot.start()