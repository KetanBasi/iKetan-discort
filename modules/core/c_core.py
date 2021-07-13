import os
import random
import configparser
from typing import List, Union
from typing.io import TextIO

from discord.errors import Forbidden

configuration = """[base]
name            = bot - iKetan
version         = 0.1
description     = iKetan Discord Bot
owner           = KetanBasi#5473
prefix          = ketan.
adminPrefix     = ketan$

[operation]
cycleStatus     = true
; delay in ms | 1 s = 1000 ms
CStatusDelay    = 5000
"""

global botName, botVersion, botDescription, botOwner
global prefix, adminPrefix, cycleStatus, CStatusDelay


def is_owner(user) -> bool:
    owners = read_file('owner')
    return user in owners


def read_file(file, raw=False) -> Union[TextIO, List[str], None]:
    try:
        with open(file, 'r') as _file:
            if raw:
                return _file
            else:
                return [i.strip() for i in _file.readlines()]
    except FileNotFoundError:
        return None


def getRandom(file) -> str:
    wordList = read_file(f'assets/{file}')
    return random.choice(wordList)


def readConfig(file) -> (tuple, tuple):
    global botName, botVersion, botDescription, botOwner
    global prefix, adminPrefix, cycleStatus, CStatusDelay

    # DESC: Read config file
    config = configparser.ConfigParser()
    config.read(file)

    # DESC: [Base] section
    config.base = config['base']
    botName = config.base.get('name', 'bot - iketan')
    botVersion = config.base.getfloat('version', '0.1')
    botDescription = config.base.get('description', 'an iKetan bot')
    botOwner = config.base.get('owner', '')
    prefix = config.base.get('prefix', 'ketan.')
    adminPrefix = config.base.get('adminPrefix', 'ketan#')

    # DESC: [operation] section
    config.operation = config['operation']
    cycleStatus = config.operation.getboolean('cycleStatus', False)
    CStatusDelay = config.operation.getint('CStatusDelay', 5000)

    # DESC: return all vars
    return (
               botName,
               botVersion,
               botDescription,
               botOwner,
               prefix,
               adminPrefix
               ), (
               cycleStatus,
               CStatusDelay
        )


def createConfig(mode) -> bool:
    try:
        with open('config.ini', mode) as configFile:
            configFile.write(configuration)
        return True
    except FileNotFoundError:
        return False


def get_token(tokenName: str) -> str:
    try:
        # DESC: Get secret token from environment variable
        return os.environ[tokenName]
    except KeyError:
        try:
            with open(tokenName, 'r') as tokenSource:
                return tokenSource.read().strip()
        except FileNotFoundError:
            print(f'NO \'{tokenName}\' TOKEN FOUND')
            return ''


async def send_embed(target, embed):
    try:
        await target.send(embed=embed)
    except Forbidden:
        await target.send('I can\'t send embeds message here. '
                          + 'Would you mind to check my permission '
                          + 'or report your server administrator?'
                          )
