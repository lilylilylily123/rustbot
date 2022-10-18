import os
import discord
from rustplus import RustSocket

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)
from dotenv import load_dotenv
socket = RustSocket("209.237.141.22", "28019", 76561198815346499, -111167879)

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
    channel = bot.get_channel(1018219976521429043)
    await channel.send(f"Welcome {member.mention} to ``{member.guild}``!")
@bot.slash_command()
async def ping(ctx):
    await ctx.respond(f"🏓 Pong ({round(bot.latency * 1000)}ms)")
@bot.slash_command()
async def kick(ctx, user: discord.Member, *, reason = None):
    if ctx.author.guild_permissions.ban_members:
        if not reason:
            await user.kick()
            await ctx.respond(f"**{user}** has been kicked for *no reason*.")
        else:
            await user.kick(reason=reason)
            await ctx.respond(f"**{user}** has been kicked for *{reason}*.")
    else:
        await ctx.respond(f"You don't have permissions, you silly little cheater!")
@bot.slash_command()
async def poof(ctx, user: discord.Member, *, reason = None):
    if ctx.author.guild_permissions.ban_members:
        if not reason:
            await user.ban()
            await ctx.respond(f"**{user}** has been banned for *no reason*.")

        else:
            await user.ban(reason=reason)
            await ctx.respond(f"**{user}** has been banned for *{reason}*.")
    else:
        await ctx.respond(f"You don't have permissions, you silly little cheater!")
@bot.slash_command()
async def jailtime(ctx, user: discord.Member):
    if ctx.author.guild_permissions.ban_members:
        role = discord.utils.get(ctx.guild.roles, name="Calvin Jail Time")
        channel = bot.get_channel(1030211029621293136)
        voice_state = user.voice

        if voice_state is None:
            await user.add_roles(role)
            await ctx.respond(f"{user.mention} has been put into jail. hehehehehe :) put in jail!")
        else:
            await user.move_to(channel)
            await user.add_roles(role)
            await ctx.respond(f"{user.mention} has been put into jail. hehehehehe :) put in jail!")
    else:
        await ctx.respond(f"You don't have permissions, you silly little cheater!")
@bot.slash_command()
async def unjailtime(ctx, user: discord.Member):
    if ctx.author.guild_permissions.ban_members:
        role = discord.utils.get(ctx.guild.roles, name="Calvin Jail Time")
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.respond(f"{user.mention} has been removed from jail. good dog!!!!!!!!!!! :dog: :dog:")
        else:
            await ctx.respond(f"{user.mention} is not in jail. tf u smokin bro?? are you gio???")
    else:
        await ctx.respond(f"You don't have permissions, you silly little cheater!")
@bot.slash_command()
async def map(ctx):
    map = await socket.get_map(True, True, True)
    server = await socket.get_info()
    map.save('map.png')
    embed = discord.Embed(title=f"Server Map", color=discord.colour.Color.dark_purple(), description=f"{server.name}")
    file = discord.File("map.png", filename="image.png")
    await ctx.respond(file=file, embed=embed)
    os.remove('map.png')
@bot.slash_command()
async def players(ctx):
    server = await socket.get_info()
    players = (await socket.get_info()).players
    embed = discord.Embed(title=f"Player Count", color=discord.colour.Color.dark_purple(), description=f"*{server.name}*\n \n There are **{players}** players online.")
    await ctx.respond(embed=embed)
@bot.slash_command()
async def server(ctx):
    map = await socket.get_map(True, True, True)
    server = await socket.get_info()
    players = (await socket.get_info()).players
    map.save('map.png')
    time = (await socket.get_time()).time
    embed = discord.Embed(title=f"**Server Info**", color=discord.colour.Color.dark_purple(), description=f"*{server.name}*\n \n There are **{players}** players online, with the time being **{time}**.")
    file = discord.File("map.png", filename="image.png")
    await ctx.respond(file=file, embed=embed)
    os.remove('map.png')


bot.run(TOKEN)