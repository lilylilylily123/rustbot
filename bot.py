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


async def time():
    print(f"It is {(await socket.get_time()).time}")


async def serverinfo():
    print(f"{(await socket.get_info()).players}")


@client.event
async def on_ready():
    print(f'connected as: {client.user}')
    await socket.connect()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$players'):
        players = (await socket.get_info()).players
        await message.channel.send(f"There are {players} players online!")

client.run(TOKEN)