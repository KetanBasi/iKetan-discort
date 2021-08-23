import json
import random

import requests

from modules.core import c_core

unsplash_link = "https://unsplash.com/" "?utm_source=iKetan-dct&utm_medium=referral"
unsplash_base = "https://api.unsplash.com/"
api_query = "?client_id={0}&query={1}&per_page={2}&content_filter={3}"
search_photo_api = unsplash_base + "search/photos/" + api_query
photo_api = unsplash_base + "photos/"
random_photo_api = photo_api + "random/" + api_query
token = c_core.get_token("unsplash")


class Author:
    def __init__(self, name, username, profile_pic):
        self.name = name
        self.username = username
        self.profile_pic = profile_pic

    def __str__(self):
        return self.name


class Link:
    def __init__(self, source, download, thumbnail, author):
        self.source = source
        self.download = download
        self.thumbnail = thumbnail
        self.author = author

    def __str__(self):
        return self.source


class Color:
    def __init__(self, red, green, blue):
        self.red: int = red
        self.green: int = green
        self.blue: int = blue

    def __str__(self):
        return f"{self.red}, {self.green}, {self.blue}"


class Dimension:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __str__(self):
        return f"{self.width}x{self.height}"


class Image:
    def __init__(
        self,
        _id: str,
        desc: str,
        author: Author,
        color: Color,
        link: Link,
        tags: list,
        dimension: Dimension,
        likes: int,
    ):
        self._id = _id
        self.desc = desc.capitalize()
        self.author = author
        self.color = color
        self.link = link
        self.tags = tags
        self.dimension = dimension
        self.likes = likes

    def __str__(self):
        return f"{self._id}: {self.desc}"


def find_image(keyword="", content_filter="high", _random=False):
    limit = 10

    if not _random:
        link = search_photo_api.format(token, keyword, limit, content_filter)
        response = requests.get(link)
        content = json.loads(response.content)

        if response.status_code != 200 or "errors" in content:
            raise RuntimeError(f"Response Error: {response.status_code}")

        position = (random.randint(1, 10) if content["total"] >= limit else
                    random.randint(1, content["total"]))
        pic = content["results"][position]
        desc = (pic["description"]
                if pic["description"] and len(pic["description"].split()) > 1
                else pic["alt_description"])
        tags = [tag["title"] for tag in pic["tags"]]

    else:
        link = random_photo_api.format(token, keyword, limit, content_filter)
        response = requests.get(link)
        pic = json.loads(response.content)

        if response.status_code != 200 or "errors" in pic:
            raise RuntimeError(f"Response Error: {response.status_code}")

        desc = (pic["description"]
                if pic["description"] and len(pic["description"].split()) > 1
                else pic["alt_description"])
        tags = []

    return Image(
        _id=pic["id"],
        desc=desc,
        author=Author(
            name=pic["user"]["name"],
            username=pic["user"]["username"],
            profile_pic=pic["user"]["profile_image"]["small"],
        ),
        color=Color(
            red=int(pic["color"][1:3], 16),
            green=int(pic["color"][3:5], 16),
            blue=int(pic["color"][5:7], 16),
        ),
        link=Link(
            source=pic["links"]["html"] + "?utm_source=iKetan-dct"
            "&utm_medium=referral",
            download=pic["links"]["download"],
            thumbnail=pic["urls"]["small"],
            author=pic["user"]["links"]["html"] + "?utm_source=iKetan-dct"
            "&utm_medium=referral",
        ),
        tags=tags,
        dimension=Dimension(width=pic["width"], height=pic["height"]),
        likes=pic["likes"],
    )
