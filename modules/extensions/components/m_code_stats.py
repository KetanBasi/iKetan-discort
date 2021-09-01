import json
import requests
from datetime import datetime
from typing import Tuple, Dict

code_stats = "https://codestats.net/"
cs_api = code_stats + "api/"
cs_user = cs_api + "users/"


class UserStats:
    def __init__(
            self, username: str, user_page: str, max_stat: Tuple[str, int],
            languages: Dict[str, int], total_xp: int,
            new_xp: int, last_code: datetime, machines: Dict[str, int]
            ):
        self.username = username
        self.user_page = user_page
        self.max_stat = max_stat
        self.languages = languages
        self.total_xp = total_xp
        self.new_xp = new_xp
        self.last_code = last_code
        self.machines = machines
    
    def __str__(self):
        return f"{self.username}: {self.total_xp}"


def get_user_stats(username) -> UserStats:
    url = cs_user + username
    response = requests.get(url=url)
    
    if response.status_code == 200:
        content = json.loads(response.content)
        
        if "error" in content:
            raise RuntimeError(content["error"])
        
        stat = {}
        for language in content["languages"]:
            stat[language] = content["languages"][language]["xps"]
        
        highest = max(stat, key=stat.get)
        return UserStats(
            username=content["user"],
            user_page=code_stats + "/users/" + username,
            max_stat=(highest, stat[highest]),
            languages=stat,
            total_xp=content["total_xp"],
            new_xp=content["new_xp"],
            last_code=max(content["dates"]),
            machines=content["machines"]
            )
    
    elif 400 <= response.status_code < 500:
        err_msg = f"{response.status_code}"
        
        if response.status_code == 404:
            err_msg += f": {username}"
        
        raise RuntimeError(err_msg)
