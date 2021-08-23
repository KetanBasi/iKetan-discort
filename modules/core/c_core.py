import configparser
import os
import platform
import random
import tempfile
from datetime import datetime
from typing import List, Union
from typing.io import TextIO

main_location = os.path.normpath(f"{os.path.dirname(__file__)}/../..")

if ".env" in os.listdir(main_location):
    from dotenv import load_dotenv

    # ? Load .env file
    load_dotenv(main_location)

# ? ==================
# ? Notes
# ? ==================

#

# ? ==================
# ? Define Variables
# ? ==================

# * Characters for pretty_print()
corner_top_left = "╔"
corner_top_right = "╗"
corner_bottom_left = "╚"
corner_bottom_right = "╝"
hor_double = "═"
hor_double_divide_left = "╠"
hor_double_divide_right = "╣"
hor_single = "─"
hor_single_divide_left = "╟"
hor_single_divide_right = "╢"
ver_double = "║"

# * Default config
default_config = """[base]
name                = Unnamed iKetan bot
version             = 0.1
description         = iKetan Discord Bot
owner               = KetanBasi#5473
prefix              = ketan.
admin_prefix        = ketan$

[operation]
cycle_status        = true
; delay in ms | 1 s = 1000 ms
cycle_status_delay  = 5000
"""


class BotInfo:
    def __init__(
        self,
        name,
        version,
        description,
        owner,
        prefix,
        adminPrefix,
        cycleStatus,
        CStatusDelay,
    ):
        self.name = name
        self.version = version
        self.description = description
        self.owner = owner
        self.prefix = prefix
        self.admin_prefix = adminPrefix
        self.cycle_status = cycleStatus
        self.cycle_status_delay = CStatusDelay

    def __str__(self):
        return self.name


# ? ==================
# ? Functions
# ? ==================
# def


def is_owner(user) -> bool:
    """
    Check if user is bot owner
    """
    owners = get_token("owner")
    return user in owners


def read_file(file, raw=False) -> Union[TextIO, List[str], None]:
    """
    To read a file, get either raw file or list of lines
    """
    try:
        with open(file, "r") as _file:
            if raw:
                return _file
            return [i.strip() for i in _file.readlines()]

    except FileNotFoundError:
        return None


def get_random(file) -> str:
    """
    Get random line from a file
    """
    word_list = read_file(f"assets/{file}")
    return random.choice(word_list)


def create_config(mode) -> bool:
    """
    create config file and fill it with provided default value
    """
    try:
        with open("config.ini", mode) as config_file:
            config_file.write(default_config)
        return True

    except FileNotFoundError:
        return False


def read_config(file) -> BotInfo:
    """
    Read config file
    """
    # * Read config file
    config = configparser.ConfigParser()
    config.read(file)

    try:
        config.read(file)

    except Exception as error:
        if create_config(mode="w"):
            config.read(file)

        else:
            raise error

    config.base = config["base"]
    config.operation = config["operation"]
    new_bot_info = BotInfo(
        config.base.get("name", "bot - iketan"),
        config.base.getfloat("version", "0.1"),
        config.base.get("description", "an iKetan bot"),
        config.base.get("owner", ""),
        config.base.get("prefix", "ketan."),
        config.base.get("admin_prefix", "ketan#"),
        config.operation.getboolean("cycle_status", False),
        config.operation.getint("cycle_status_delay", 5000),
    )
    return new_bot_info


def get_token(tokenName: str) -> Union[str, None]:
    """
    get token from OS environment, read a file if not found
    """
    try:
        return os.environ.get(tokenName)

    except KeyError:
        # try:
        #     # with open(tokenName, 'r') as token_source:
        #     #     return token_source.read().strip()
        # except FileNotFoundError:
        print(f"NO '{tokenName}' TOKEN FOUND")
        return None


def time(get_date=True, get_time=True):
    time_format = "%Y-%m-%d " if get_date else ""
    time_format += "%H.%M.%S" if get_time else ""
    return datetime.now().strftime(time_format.strip())


# ? Each line length should be less than 52-78 characters long,
# ?     including spaces and always use space instead of tabs
# ?     for better output result (based on default terminal setting
# ?     which may vary for each device)
def pretty_print(text_list: list):
    max_len = max([len(max(text_block, key=len))
                   for text_block in text_list]) + 2
    text_list_len = len(text_list)

    top_edge = corner_top_left + hor_double * max_len + corner_top_right + "\n"
    main_divide = (hor_double_divide_left + hor_double * max_len +
                   hor_double_divide_right + "\n")
    bottom_edge = corner_bottom_left + hor_double * max_len + corner_bottom_right

    result_text = top_edge

    for i_block in range(text_list_len):
        for line in text_list[i_block]:
            right_spaces = " " * (max_len - len(line) - 1)
            result_text += ver_double + " " + line + right_spaces + ver_double
            result_text += "\n"

        if i_block != text_list_len - 1:
            result_text += main_divide

    result_text += bottom_edge
    print(result_text)


# ? ==================
# ? Addl Variables
# ? ==================

this_machine = platform.system()
this_python = platform.python_version()
this_bot = read_config("config.ini")

my_work_dir = os.path.join(tempfile.gettempdir(), this_bot.name)
