import logging
import os
from datetime import datetime

import discord
from discord.ext import commands, tasks

# ? Load this bot's components/modules
from modules.core import c_core
from modules.extensions.components import m_tenor

# * Bot token name on Environment Variable
bot_token = "iketan_token"

# ? ==================
# ? Notes
# ? ==================

# TODO: Implement separated guild admin-only prefix
# TODO: Implement guild admin-only commands
# TODO: Implement database (MongoDB) integration
# TODO: Doc everything on separate docs and/or give it proper comments
# TODO: Clean up & rearrange everything
# TODO: Deploy, mdf

# ? ==================
# ? Declare Variables
# ? ==================

this_bot = c_core.this_bot
my_work_dir = c_core.my_work_dir

# ? ==================
# ? Setup work dir
# ? ==================

try:
    os.mkdir(my_work_dir)
except FileExistsError:
    pass

# ? ==================
# ? Setup Logging
# ? ==================

dct_logger = logging.getLogger("discord")
dct_logger.setLevel(logging.DEBUG)

# for _dir in ['.', '/tmp']:
#     if os.path.exists(f'{_dir}/iKetan-dct'):
#         _dir += '/iKetan-dct'
#     if os.access(_dir, os.W_OK):
#         location = _dir
#         break

# * Logging: File Handler
# * ==================
log_file = os.path.join(*[my_work_dir, this_bot.name + " " + c_core.time()])
log_file_handler = logging.FileHandler(filename=f"{log_file}.log",
                                       encoding="utf-8",
                                       mode="w")
log_file_handler.setLevel(logging.DEBUG)

# * Logging: Console Handler
# * ==================
log_console_handler = logging.StreamHandler()
log_console_handler.setLevel(logging.ERROR)

# * Logging: Formatter
# * ==================
log_format = logging.Formatter(
    "[%(asctime)s | %(levelname)s] %(name)s: %(message)s")
log_file_handler.setFormatter(log_format)
log_console_handler.setFormatter(log_format)

# * Logging: Add handlers
# * ==================
dct_logger.addHandler(log_file_handler)
dct_logger.addHandler(log_console_handler)

# ? ==================
# ? Declare Other Variable
# ? ==================

intent = discord.Intents.all()
# client = discord.Client()
bot = commands.Bot(
    command_prefix=(this_bot.prefix, this_bot.admin_prefix),
    description=this_bot.description,
    help_command=None,
    intents=intent,
)
counter = -1

# ? ==================
# ? Main Bot : Load all available modules
# ? ==================

module_loaded = []
module_dir = ["system", "extensions"]

for subdir in module_dir:
    for item in os.listdir(f"modules/{subdir}"):
        if item.endswith(
                ".py") and item != "components" and not item.startswith("_"):
            bot.load_extension(f"modules.{subdir}.{item[:-3]}")
            print(f"loaded: {item}")
            module_loaded.append(item)

# ? ==================
# ? Main Bot : On Event
# ? ==================


# * Event: When the bot was ready to use
# * ==================
@bot.event
async def on_ready():
    """
    Do something when bot is ready
    """
    global bot_owner

    # * Login report
    # * ==================
    # ? Each line length should be less than 52-78 characters long,
    # ?     including spaces and always use space instead of tabs
    # ?     for better output result (based on default terminal setting
    # ?     which may vary for each device)
    reports = [
        [f"Logged in as : {bot.user}"],
        [
            f"Name         : {this_bot.name}",
            f"Ver.         : {this_bot.version}",
            f"ID           : {bot.user.id}",
            f"Owner        : {this_bot.owner}",
            f"Prefix       : {this_bot.prefix}",
            f"Adm. Prefix  : {this_bot.admin_prefix}",
        ],
        [
            f"Platform     : {c_core.this_machine}",
            f"Python       : {c_core.this_python}",
            f"Work Dir     : {c_core.my_work_dir}",
        ],
        ["Module loaded:"] + module_loaded,
    ]

    c_core.pretty_print(reports)

    # * Bot Activity
    # * ==================
    # ? Either functions below gives similar result
    # ! Discord bot can't have rich presence feature like app logo or etc.

    # * This one use discord.Game() to make it looks like playing something
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name="my little ram on rem - Pre-Alpha discord bot",
            start=datetime.now()),
    )

    # * This one use discord.Activity() and discord.ActivityType.listening
    # *     as its type of activity, so it looks like listening to something
    # await bot.change_presence(
    #         status=discord.Status.online,
    #         activity=discord.Activity(
    #                 name="your words",
    #                 type=discord.ActivityType.listening
    #                 )
    #         )

    dct_logger.info("Success Login")
    bot_owner = await bot.fetch_user(int(c_core.get_token("owner")))
    _embed = discord.Embed(
        title=c_core.get_random("greetings"),
        description=c_core.time(),
        colour=discord.Colour.from_rgb(r=255, g=255, b=255),
    )
    _embed.set_image(url=m_tenor.test())
    await bot_owner.send(embed=_embed)
    # await cycle.start()


# * Event: When command error occur
# * ==================
# @bot.event
# async def on_command_error(ctx, error):
#     print(f"⇒ Error: {error}")
#     await ctx.send(f"> Hold up, can't process: {str(error)}")

# ? ==================
# ? Main Bot : Loop tasks
# ? ==================


@tasks.loop(seconds=30)
async def cycle():
    """
    Cycle function
    """
    global counter
    counter += 1
    _name = f"I'm awake for {counter}0 secs"
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name=_name))


# ? ==================
# ? Main Bot : Commands
# ? ==================

# * >>==> Put your "uncategorized" commands here. <<=<< *

# ? ==================
# ? Run the Bot
# ? ==================

bot.run(c_core.get_token(bot_token))
