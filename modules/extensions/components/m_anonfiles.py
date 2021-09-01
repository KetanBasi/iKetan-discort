import json
import requests

_anonfile_api = "https://api.anonfiles.com/upload"
_anonfile_check = "https://api.anonfiles.com/v2/file/{0}/info"


class AnonFiles:
    def __init__(self):
        self.success: bool = False
        self.link: str = ""
        self.file_id: str = ""
        self.file_name: str = ""
        self.file_size: int = -1
        self.msg: str = ""
    
    def _wrap(self, response):
        data = json.loads(response.content)
        self.success = data["status"]
        
        if 200 <= response.status_code < 300:
            self.link = data["data"]["file"]["url"]["short"]
            self.file_id = data["data"]["file"]["metadata"]["id"]
            self.file_name = data["data"]["file"]["metadata"]["name"]
            self.file_size = data["data"]["file"]["metadata"]["size"]["bytes"]
        
        elif response.status_code == 404:
            self.msg = data["error"]["message"]
        
        else:
            raise RuntimeError(f"{response.status_code}: {response.content}")

    def upload(self, file):
        file = {"file": open(file, "rb")}
        # file = {"file": file}
        response = requests.post(_anonfile_api, files=file)
        self._wrap(response)
        return

    def check_status(self, file_id):
        link = _anonfile_check.format(file_id)
        response = requests.get(link)
        self._wrap(response)
        return
