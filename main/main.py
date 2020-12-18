import discord
import discord.ext
import components.modules

# To Invite this bot to your server:
# https://discordapp.com/oauth2/author/authorize?client_id=<Bot Client ID>&scope=bot&permission=8
# Use link above, change the <Bot Client ID> with
#  your Bot Client ID on Discord Developers page

def read_sc_token():
    with open('token', 'r') as token_file:
        lines = f.readlines()
        return lines[0].strip()

token = read_sc_token()
client = discord.Client()

command_prefix = "$"
mcon = components.modules

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(command_prefix):
        commands = message.content.split()
        command = commands[0][1:].lower()

        if command == "say" and commands:
            # await message.channel.send(commands[1:])
            await message.channel.send(mcon.say(commands[1:]))

        elif command == "knock":
            await message.channel.send("Who's there?")

client.run(token)

# await client.change_presence(activity=discord.Game(name="KetanBot Beta Ver."))
