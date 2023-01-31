import requests
from token_api import token_api


class behind_the_name_api(token_api):
    def get_related_names(self, name):
        name_query = "https://www.behindthename.com/api/related.json"

        parameters = {"name": name, "key": self.API_TOKEN}

        name_list_response = requests.get(name_query, params=parameters)

        names = name_list_response.json()["names"]

        return names
