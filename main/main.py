import re, os, discord, config
from discord import state
from discord import message
import discord.ext
from datetime import datetime
from config import RelAlpha, RelBeta
# from datetime import time
# from modules import say
# import components.modules as mcon

# To Invite this bot to your server:
# https://discordapp.com/oauth2/author/authorize?client_id=<Bot Client ID>&scope=bot&permission=8
# Use link above, change the <Bot Client ID> with
#  your Bot Client ID on Discord Developers page

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
    if RelAlpha or RelBeta:
        if user != None:
            user = f'user[{user}]: '
        if command != None:
            command = f'running command: [{command}]'
        with open('bot.log', 'a') as logFile:
            if error != None:
                logFile.write(f'''[{datetime.now()}]: ERROR: {error}
                \t{user}{command}\n''')
            else:
                logFile.write(f'''[{datetime.now()}]: {user}{command}
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
    # ANCHOR: Login status
    print("We have logged in as {0.user}".format(client))
    # ANCHOR: Change Presence
    # game = discord.Game("with the API")
    # await client.change_presence(status=discord.Status.idle, activity=game)
    # await client.change_presence(status=discord.Status.online, activity=discord.Game(name="KetanBot Beta Alpha 1.0.4", state='In Game', party={'id': 0, 'size': [5, 5]}))
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='KetanBot-X on my own device'))
    # await client.change_presence(status=discord.Status.online, activity=discord.Activity(name='The duck', type=discord.ActivityType.playing, state='Co-op Party', details='Co-op Mode', timestamps={'start': 0}, large_image_text='What?', large_image_url=config.presence_image_url, small_image_text='What?', small_image_url=config.presence_image_url, party={'id': 'ae488379-351d-4a4f-ad32-2b9b01c91657', 'size': [2, 2]}))

@client.event
async def on_message(message):
    global admin_confirm
    output = ''
    # ANCHOR: Ignore self-message
    if message.author == client.user:
        print(f'{message.author} {client.user}')
        return
    # ANCHOR: Detect yes/no confirmation
    if message.content.lower() == 'yes' or message.content.lower() == 'no':
        if admin_confirm == 'shutdown':
            if message.content.lower() == 'yes':
                exit()
            else:
                admin_confirm = None
    # SECTION: Admin command
    elif message.content.startswith('##'):
        print(f'[DEV] Dev message on {message.channel}: {message.author}')
        _user_input = re.search(rf'^##(?P<command>\S*)', message.content)
        user_input = _user_input.groupdict()
        command = user_input['command'].lower()
        if command == 'shutdown':
            admin_confirm = 'shutdown'
            await message.channel.send('Confirm shutdown (yes/no)')
    # !SECTION: Admin command
    # SECTION: User command
    elif message.content.startswith(command_prefix):
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

        elif command == "knock":
            output = "Who's there?"

        else:
            output = 'Are you talking to me? I haven\'t learned that command before.'

        bot_log(f'{message.author.name}#{message.author.discriminator}', message.content, output)
        await message.channel.send(output)
    # !SECTION: User command
            

client.run(token)

