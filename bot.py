import os
import discord
intents = discord.Intents.all()

bot = discord.Bot(intents=intents)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")
@bot.event
async def on_message(message):
   if message.author == bot.user:
       return
   if message.content.startswith('gerard'):
       await message.channel.send('is gay!!!!')
   if message.content.startswith('storm'):
       await message.channel.send('is lesbian!!!!')
   if message.content.startswith('gio'):
       await message.channel.send('is high!!!!')
@bot.listen()
async def on_member_join(member):
    await member.send(f"Welcome ``{member}`` to ``{member.guild.name}``!")
@bot.slash_command()
async def ping(ctx):
    await ctx.respond(f"🏓 Pong ({round(bot.latency * 1000)}ms)")
@bot.slash_command()
async def kick(ctx, user: discord.Member, *, reason = None):
  if not reason:
    await user.kick()
    await ctx.respond(f"**{user}** has been kicked for *no reason*.")
  else:
    await user.kick(reason=reason)
    await ctx.respond(f"**{user}** has been kicked for *{reason}*.")
@bot.slash_command()
async def ban(ctx, user: discord.Member, *, reason = None):
    if not reason:
        await user.ban()
        await ctx.respond(f"**{user}** has been banned for *no reason*.")
    else:
        await user.ban(reason=reason)
        await ctx.respond(f"**{user}** has been banned for *{reason}*.")
bot.run(TOKEN)