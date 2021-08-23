import json
import random
import typing

import requests

from modules.core.c_core import get_token

# ? ==================
# ? Local Variables
# ? ==================

tenor_token = get_token("tenor")
tenor_api = ("https://g.tenor.com/v1/search?q={0}&key={1}&limit={2}" +
             "&media_filter=minimal")

# DESC: "caching" results
# TODO: Use database instead :)
gifs = {}
last_random = {}

# ? ==================
# ? Functions
# ? ==================


def _get(api, term, token, limit=20) -> requests.models.Response:
    """
    Make a request
    """
    r = requests.get(api.format(term, token, limit))
    return r


def get_gif(term, limit: typing.Optional[int] = 20) -> str:
    """
    get gif and process it
    """
    result = _get(tenor_api, term, tenor_token, limit)

    if result.status_code == 200:

        while True:
            i = random.randint(0, limit - 1)

            if term in last_random:

                if last_random[term] == i:
                    continue

            else:
                last_random[term] = i

            break

        return json.loads(
            result.content)["results"][i]["media"][0]["gif"]["url"]

    return f"*GIF source currently unavailable*: {result.status_code}"


def test() -> str:
    """
    test GIF API connection
    """
    term = "happy"
    limit = 10

    return get_gif(term, limit)
