import json
from dateutil.parser import isoparse

class UserInformation(object):
    
    def __init__(self, responseString: json) -> None:
        assert responseString["object"] == "user"
        data = responseString["data"]
        self.username = data["username"]
        self.level = data["level"]
        self.start_date = isoparse(data["started_at"])

    def __str__(self):
        return f"username : {self.username} \nlevel : {self.level}\nstart_date:{self.start_date}"