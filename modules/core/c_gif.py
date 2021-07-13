import json
import random
import typing
import requests

import discord
from discord.ext import commands, tasks

from modules.core.c_core import get_token


# ? ==================
# ? Local Variables
# ? ==================
tenorToken = get_token('tenor')
tenorApi = 'https://g.tenor.com/v1/search?q={0}&key={1}&limit={2}'\
           + '&media_filter=minimal'

# DESC: "caching" results
gifs = {}
lastRandom = {}


def _get(api, term, token, limit=20) -> requests.models.Response:
    r = requests.get(
            api.format(
                    term,
                    token,
                    limit
                    )
            )
    return r


def getGif(term, limit: typing.Optional[int] = 20) -> str:
    result = _get(tenorApi, term, tenorToken, limit)
    if result.status_code == 200:
        while True:
            i = random.randint(0, limit-1)
            if term in lastRandom:
                if lastRandom[term] == i:
                    continue
            else:
                lastRandom[term] = i
            break
        return json.loads(result.content)['results'][i]['media'][0]['gif']['url']
    else:
        return f'*GIF source currently unavailable*: {result.status_code}'


def test() -> str:
    term = "happy"
    limit = 10
    return getGif(term, limit)
