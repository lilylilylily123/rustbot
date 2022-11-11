import os
import random
import sqlite3

import discord
from discord.ext import commands
from discord.ext import tasks
from rustplus import RustSocket

con = sqlite3.connect("rustcreds.db")
cur = con.cursor()
# cur.execute("CREATE TABLE creds(ip, port, steam, rust)")

con.commit()
cooldown = []
intents = discord.Intents.all()

bot = discord.Bot(intents=intents)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


@bot.slash_command()
async def setcredentials(ctx):
    await ctx.respond(f'Please enter your name.')
    username = await bot.wait_for('message')
    cur.execute(f"CREATE TABLE IF NOT EXISTS {username.content}(ip, port, steam, rust)")
    await ctx.send(f'Please enter your rust server IP.')
    ip = await bot.wait_for('message')
    await ctx.send(f'Please enter your rust server port.')
    port = await bot.wait_for('message')
    await ctx.send(f'Please enter your steam token..')
    steam = await bot.wait_for('message')
    await ctx.send(f'Please enter your rust server token.')
    rust = await bot.wait_for('message')
    cur.execute(f"INSERT INTO {username.content}(ip, port, steam, rust) VALUES (?, ?, ?, ?)",
                (ip.content, port.content, steam.content, rust.content))
    con.commit()


socket = RustSocket("209.237.141.22", "28019", 76561198815346499, -111167879)


@bot.event
async def on_ready():
    change_status.start()
    print(f"Connected as {bot.user}")


status = ['Rust', 'with your mother', 'Rust with Storm']


@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(random.choice(status)))

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
async def kick(ctx, user: discord.Member, *, reason=None):
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
async def poof(ctx, user: discord.Member, *, reason=None):
    if ctx.author.id == '817723313605574696':
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
    embed = discord.Embed(title=f"Player Count", color=discord.colour.Color.dark_purple(),
                          description=f"*{server.name}*\n \n There are **{players}** players online.")
    await ctx.respond(embed=embed)


@bot.slash_command()
async def server(ctx):
    map = await socket.get_map(True, True, True)
    server = await socket.get_info()
    players = (await socket.get_info()).players
    map.save('map.png')
    time = (await socket.get_time()).time
    embed = discord.Embed(title=f"**Server Info**", color=discord.colour.Color.dark_purple(),
                          description=f"*{server.name}*\n \n There are **{players}** players online, with the time being **{time}**.")
    file = discord.File("map.png", filename="image.png")
    await ctx.respond(file=file, embed=embed)
    os.remove('map.png')


@bot.slash_command()
@commands.cooldown(per=3600, rate=1)
async def play(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Kids")
    global cooldown
    cooldown = False
    await ctx.respond(f"{role.mention}")


@play.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(
            f"This command is on cooldown. You will be able to use it in ``{round(error.retry_after / 60)}`` minutes.")


whitelist = [817723313605574696]


@play.after_invoke
async def reset_cooldown(ctx):
    for e in whitelist:
        if e == ctx.author.id:
            play.reset_cooldown(ctx)


bot.run(TOKEN)