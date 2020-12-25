import re, os, discord
from discord import message
import discord.ext
from datetime import datetime as dateTime
from datetime import time
# from modules import say
# import components.modules as mcon

# To Invite this bot to your server:
# https://discordapp.com/oauth2/author/authorize?client_id=<Bot Client ID>&scope=bot&permission=8
# Use link above, change the <Bot Client ID> with
#  your Bot Client ID on Discord Developers page

# value (always lowercase):
#   - alpha
#   - beta
#   - rc
#   - stable
botReleaseStatus = 'alpha'

botReleaseAlpha = botReleaseStatus == 'alpha'
botReleaseBeta = botReleaseStatus == 'beta'
botReleaseRC = botReleaseStatus == 'rc'
botReleaseStable = botReleaseStatus == 'stable'
output = ''
admin_confirm = None

def read_sc_token():
    try:
        with open('main/token', 'r') as token_file:
            lines = token_file.readlines()
            return lines[0].strip()
    except:
        with open('token', 'r') as token_file:
            lines = token_file.readlines()
            return lines[0].strip()    

# Logs available on alpha release for development purpose only
def bot_log(user, command, output=None, error=None):
    if botReleaseAlpha:
        if user != None:
            user = f'user[{user}]: '
        if command != None:
            command = f'running command: [{command}]'
        with open('bot.log', 'a') as logFile:
            if error != None:
                logFile.write(f'''[{dateTime.now()}]: ERROR: {error}
                \t{user}{command}\n''')
            else:
                logFile.write(f'''[{dateTime.now()}]: {user}{command}
                Success output: [{output}]\n''')

token = read_sc_token()
client = discord.Client()
discord_color = discord.Colour

command_prefix = "$"
man__say = '''Usage: `{0}say #channel_tag Your Words`

If you type: `{0}say Your Words`
Then I'll send `Your Words` in this channel. Or,
if you type: `{0}say #lobby Hello, I'm John`
Then I'll send `Hello, I'm John` in #lobby'''.format(command_prefix)


# def embed(description, title=None, color=discord.Colour(teal)):
def embed(description, title=None, colour=discord_color.orange(), *fields):
    _message = discord.Embed(
        title = title,
        description = description,
        colour = colour
    )
    for _item in fields:
        _message.add_field(name=_item['title'], value=_item['description'])
    return _message

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    global admin_confirm
    output = ''
    # try:
    if message.content.lower() == 'yes' or message.content.lower() == 'no':
        if admin_confirm == 'shutdown':
            if message.content.lower() == 'yes':
                exit()
            else:
                admin_confirm = None
    if message.author == client.user:
        return
    if message.content.startswith(command_prefix):
        # commands = message.content.split()
        # command = commands[0][1:].lower()
        print(f'{message.channel} {message.author}')
        _user_input = re.search(rf'^{re.escape(command_prefix)}(?P<command>\S*)\s*(?P<the_rest>.*)', message.content)
        user_input = _user_input.groupdict()
        command = user_input['command'].lower()
        the_rest = user_input['the_rest']

        if command == 'join':
            # Do something
            return
        elif command == 'say':
            if the_rest == '':
                __embed = embed(man__say, f'Command manual: {command_prefix}say')
                bot_log(f'{message.author.name}#{message.author.discriminator}', message.content, output=__embed)
                await message.channel.send(content=None, embed=__embed)
                # bot_log(f'{message.author.name}#{message.author.discriminator}', message.content)
                return
            the_channel = re.search(rf'<#(?P<the_channel>[0-9]+)>', the_rest)
            if the_channel != None:
                the_channel = the_channel.groupdict()['the_channel']
                target_channel = client.get_channel(int(the_channel))
                # channel = discord.the_channel
                # print(message.channel)
                user_message = re.search(rf'<#{re.escape(the_channel)}>\s*(?P<user_message>.*)', the_rest).groupdict()['user_message']

                bot_log(f'{message.author.name}#{message.author.discriminator}', message.content, output=user_message)
                await target_channel.send(user_message)
                return
            else:
                output = the_rest
                # await message.channel.send(the_rest)
                # bot_log(f'{message.author.name}#{message.author.discriminator}', message.content)
                # await message.channel.send(mcon.say(the_rest))

        elif command == "knock":
            output = "Who's there?"
            #await message.channel.send("Who's there?")
            #return
        else:
            output = 'Are you talking to me? I haven\'t learned that command before.'
            #await message.channel.send('Are you talking to me? I haven\'t learned that command before')
        bot_log(f'{message.author.name}#{message.author.discriminator}', message.content, output)
        await message.channel.send(output)
    # except Exception as error:
        # bot_log(f'{message.author.name}#{message.author.discriminator}', message.content, error=error)
    elif message.content.startswith('##'):
        print(f'[DEV] Dev message on {message.channel}: {message.author}')
        _user_input = re.search(rf'^##(?P<command>\S*)', message.content)
        user_input = _user_input.groupdict()
        command = user_input['command'].lower()
        if command == 'shutdown':
            admin_confirm = 'shutdown'
            await message.channel.send('Confirm shutdown (yes/no)')
            

client.run(token)

# await client.change_presence(activity=discord.Game(name="KetanBot Beta Ver."))
