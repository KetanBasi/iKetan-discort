import json
import pathlib
import requests
from datetime import datetime
from modules.core.c_core import get_token

unelma_site = "https://unelmacloud.com"
unelma_api = unelma_site + "/api/v1"
unelma_token = get_token("unelma")


class Entry:
    def __init__(self, _id, name, extension, file_type, file_size, date_modified):
        self.id = _id
        self.name = name
        self.extension = extension
        self.file_type = file_type
        self.file_size = file_size
        self.date_modified = date_modified
    
    def __str__(self):
        return self.name


def entries():
    unelma_entries = unelma_api + "/entries"
    header = {
        "accept": "application/json",
        "Authorization": f"Bearer {unelma_token}"
        }
    response = requests.get(url=unelma_entries, headers=header)
    print(response.status_code)
    if response.status_code == 200:
        content = json.loads(response.content)
        data = content["data"]
        return [Entry(
            _id=file["id"],
            name=file["name"],
            extension=file["extension"],
            file_type=file["type"],
            file_size=file["file_size"],
            date_modified=file["updated_at"]
            ) for file in data]
    message = "Unauthorized" if response.status_code == 403 else "Unauthenticated"
    raise RuntimeError(message)


def upload(file):
    unelma_upload = unelma_api + "/uploads"
    header = {
        "accept": "application/json",
        "Authorization": f"Bearer {unelma_token}",
        "Content-Type": "multipart/form-data"
        }
    file = {"file": open(file, "rb")}
    response = requests.post(url=unelma_upload, headers=header, files=file)
    if response.status_code == 201:
        content = json.loads(response.content)
        print(content)
