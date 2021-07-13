import os
import logging

import discord
from discord.ext import commands, tasks

from modules.core import c_core, c_gif


# ? ==================
# ? Notes
# ? ==================

#   To Invite this bot to your server
#   https://discordapp.com/oauth2/author/authorize?client_id=<Bot Client ID>&scope=bot&permission=<permission>
#   Use link above, change the <Bot Client ID> with
#       your Bot Client ID on Discord Developers page
#       and <permission> with your desired permission
#       for your bot (discord dev portal for more).

# TODO: Implement separated guild admin-only prefix
# TODO: Implement guild admin-only commands
# TODO: Implement database (MongoDB) integration
# TODO: Release as alpha on cloud
# TODO: Clean up & rearrange everything
# TODO: Document everything on separate docs, or give it proper comments


# ? ==================
# ? Def bot sys
# ? ==================

def embed(description, title=None, colour=discord.Colour.orange(), *fields):
    _message = discord.Embed(title=title,
                             description=description,
                             colour=colour
                             )
    for _item in fields:
        _message.add_field(name=_item['title'],
                           value=_item['description']
                           )
    return _message


# ? ==================
# ? Setup Logging
# ? ==================

dctLogger = logging.getLogger('discord')
dctLogger.setLevel(logging.DEBUG)

# * Logging: File Handler
# * ==================
logFHandler = logging.FileHandler(
        filename='iKetan-dct.log',
        encoding='utf-8',
        mode='w'
        )
logFHandler.setLevel(logging.DEBUG)

# * Logging: Console Handler
# * ==================
logCHandler = logging.StreamHandler()
logCHandler.setLevel(logging.ERROR)

# * Logging: Formatter
# * ==================
logFormat = logging.Formatter(
        '[%(asctime)s | %(levelname)s] %(name)s: %(message)s'
        )
logFHandler.setFormatter(logFormat)
logCHandler.setFormatter(logFormat)

# * Logging: Add handlers
# * ==================
dctLogger.addHandler(logFHandler)
dctLogger.addHandler(logCHandler)

# ? ==================
# ? Read Config
# ? ==================

global _base, _operation
try:
    _base, _operation = c_core.readConfig('config.ini')
    dctLogger.info('Config loaded')
except (NameError, KeyError):
    dctLogger.error('Config file/key not found, attempting to create the file')
    if c_core.createConfig(mode='w'):
        _base, _operation = c_core.readConfig('config.ini')
    else:
        dctLogger.error('Cannot create config file')
        exit(1)
finally:
    botName, botVersion, botDescription, botOwner, prefix, adminPrefix = _base
    cycleStatus, CStatusDelay = _operation

# ? ==================
# ? Declare Other Variable
# ? ==================

intent = discord.Intents.all()
# client = discord.Client()
bot = commands.Bot(command_prefix=(prefix, adminPrefix),
                   description=botDescription,
                   help_command=None,
                   intents=intent
                   )
counter = 0


# ? ==================
# ? Main Bot : Load all available modules
# ? ==================

module_dir = ['administration', 'extensions']
for subdir in module_dir:
    for module in os.listdir(f'modules/{subdir}'):
        if module.endswith('.py'):
            bot.load_extension(f'modules.{subdir}.{module[:-3]}')


# ? ==================
# ? Main Bot : Functions
# ? ==================

async def _send(user: discord.User, msg):
    await user.send(msg)


async def _chp(status):
    await bot.change_presence(
            status=discord.Status.online,
            activity=status
            )


# ? ==================
# ? Main Bot : On Event
# ? ==================

@bot.event
async def on_ready():
    global botOwner
    print("We have logged in as {0.user}".format(bot))
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name='iKetan now alive')
                              )
    print(f'Bot id: {bot.user.id}')
    dctLogger.info('Success Login')
    botOwner = await bot.fetch_user(int(c_core.get_token('owner')))
    _embed = discord.Embed(title=c_core.getRandom('greetings'),
                           colour=discord.Colour.from_rgb(r=255,
                                                          g=255,
                                                          b=255
                                                          )
                           )
    _embed.set_image(url=c_gif.test())
    await botOwner.send(embed=_embed)
    await cycle.start()


# ? ==================
# ? Main Bot : Loop tasks
# ? ==================

@tasks.loop(seconds=30)
async def cycle():
    global counter
    counter += 1
    _name = f'I\'m alive for {counter}0 secs'
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name=_name))


# ? ==================
# ? Main Bot : Commands
# ? ==================
# You can put your "uncategorized" commands here.


# ? ==================
# ? Run the Bot
# ? ==================
bot.run(c_core.get_token('ketan_token'))
