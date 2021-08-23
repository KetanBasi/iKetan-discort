import json
import typing

import requests

agify_api = "https://api.agify.io/?name="
nationalize_api = "https://api.nationalize.io?name="

# ? ==================
# ? Data Class
# ? ==================


class Nation:
    def __init__(self, country_id, probability):
        self.country_id = country_id
        self.probability = probability

    def __str__(self):
        return f"{self.country_id}: {self.probability}"


# ? ==================
# ? Functions
# ? ==================


def get_age(name: str) -> int:
    result = requests.get(agify_api + name)
    content = json.loads(result.content)

    if result.status_code == 200 and "age" in content:
        return content["age"]
    raise RuntimeError(content["error"])


def get_nation(name: str) -> list:
    result = requests.get(nationalize_api + name)
    content = json.loads(result.content)

    if result.status_code == 200 and "country" in content:
        # ? return list of Nation
        return [
            Nation(country_id=country["country_id"],
                   probability=country["probability"])
            for country in content["country"]
        ]

    raise RuntimeError(result.status_code)
