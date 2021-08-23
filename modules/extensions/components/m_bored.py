import json
import os
import pprint
import sys
import typing

import requests

api_url = "https://boredapi.com/api/activity?participants={}"


class Activity:
    def __init__(self, activity, key, link, participants, _type):
        self.activity = activity
        self.key = key
        self.link = link
        self.participants = participants
        self.type = _type

    def __str__(self):
        return f"{self.type}, {self.participants} participants: {self.activity}"


def get_activity(participants: typing.Union[int, str] = ""):
    link = api_url.format(participants)
    result = requests.get(link)
    content = json.loads(result.content)

    if result.status_code != 200 or "error" in content:
        raise RuntimeError(f"Response Error: {result.status_code}")

    return Activity(
        activity=content["activity"],
        key=content["key"],
        link=content["link"],
        participants=content["participants"],
        _type=content["type"],
    )
