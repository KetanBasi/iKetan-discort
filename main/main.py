import re
import discord
from discord import message
import discord.ext
import components.modules

# To Invite this bot to your server:
# https://discordapp.com/oauth2/author/authorize?client_id=<Bot Client ID>&scope=bot&permission=8
# Use link above, change the <Bot Client ID> with
#  your Bot Client ID on Discord Developers page

def read_sc_token():
    with open('main/token', 'r') as token_file:
        lines = token_file.readlines()
        return lines[0].strip()

token = read_sc_token()
client = discord.Client()

command_prefix = "$"
mcon = components.modules

man__say = '''Usage: `{0}say #channel_tag Your Words`

If you type: `{0}say Your Words`
Then I'll send `Your Words` in this channel. Or,
if you type: `{0}say #lobby Hello, I'm John`
Then I'll send `Hello, I'm John` in #lobby'''.format(command_prefix)

# color_teal = discord.Colour.teal
# color_teal = discord.Colour.
# color_teal = discord.Colour
# color_teal = discord.Colour
# color_teal = discord.Colour
# color_teal = discord.Colour

# def embed(description, title=None, color=discord.Colour(teal)):
def embed(description, title=None, colour=0, *fields):
    _message = discord.Embed(
        title = title,
        description = description,
        colour = colour
    )
    for _item in fields:
        _message.add_field(title=_item['title'], description=_item['description'])
    return _message

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(command_prefix):
        # commands = message.content.split()
        # command = commands[0][1:].lower()
        print(message.channel)
        _user_input = re.search(rf'^{re.escape(command_prefix)}(?P<command>\S*)\s*(?P<the_rest>.*)', message.content)
        user_input = _user_input.groupdict()
        command = user_input['command'].lower()
        the_rest = user_input['the_rest']

        if command == "say":
            if the_rest == '':
                # await message.channel.send(embed(description=man__say, title='Say command manual'))
                # __embed = discord.Embed(title='eyy', description='Say something', colour=0x1abc9c)
                __embed = embed(man__say, f'Command manual: {command_prefix}say')
                await message.channel.send(content=None, embed=__embed)
                return
            # Channel tag = <#735097009136074832>
            what_to_say = re.search(rf'<>', the_rest)
            await message.channel.send(the_rest)
            # await message.channel.send(mcon.say(the_rest))

        elif command == "knock":
            await message.channel.send("Who's there?")

client.run(token)

# await client.change_presence(activity=discord.Game(name="KetanBot Beta Ver."))
