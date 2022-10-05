import discord
import os
from dotenv import load_dotenv
from rustplus import RustSocket

socket = RustSocket("209.237.141.22", "28019", 76561198815346499, -111167879)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'connected as: {client.user}')
    await socket.connect()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('gerard'):
        await message.channel.send('is gay!!!!')

    if message.content.startswith('storm'):
        await message.channel.send('is lesbian!!!!')

    if message.content.startswith('?map'):
        map = await socket.get_map(True, True, True)
        server = await socket.get_info()
        map.save('map.png')
        embed = discord.Embed(title=f"Server Map", color=discord.colour.Color.dark_purple(), description=f"{server.name}")
        file = discord.File("map.png", filename="image.png")
        await message.channel.send(file=file, embed=embed)
        os.remove('map.png')

    if message.content.startswith('?players'):
        server = await socket.get_info()
        players = (await socket.get_info()).players
        embed = discord.Embed(title=f"Player Count", color=discord.colour.Color.dark_purple(), description=f"*{server.name}*\n \n There are **{players}** players online.")
        await message.channel.send(embed=embed)

    if message.content.startswith('?server'):
        map = await socket.get_map(True, True, True)
        server = await socket.get_info()
        players = (await socket.get_info()).players
        map.save('map.png')
        time = (await socket.get_time()).time
        embed = discord.Embed(title=f"**Server Info**", color=discord.colour.Color.dark_purple(), description=f"*{server.name}*\n \n There are **{players}** players online, with the time being **{time}**.")
        file = discord.File("map.png", filename="image.png")
        await message.channel.send(file=file, embed=embed)
        os.remove('map.png')

@client.event
async def dm(message, member):
    if message.content.startswith('?playerdetails'):
        playertoken = socket.player_token
        serverip = socket.ip
        serverport = socket.port
        steamid = socket.steam_id
        await create_dm(user)
        await dm_channel.send(f'{playertoken} {serverip} {serverport} {steamid}')

client.run(TOKEN)



