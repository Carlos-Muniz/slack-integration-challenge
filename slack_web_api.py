import requests
from token_api import token_api


class slack_web_api(token_api):
    def __init__(self, *args, **kwargs):
        super(slack_web_api, self).__init__(*args, **kwargs)
        self.HEADERS = {
            "Authorization": f"Bearer {self.API_TOKEN}",
        }

    def get_available_user_ids(self):
        user_query = "https://slack.com/api/users.list"

        user_list_response = requests.get(user_query, headers=self.HEADERS)

        user_list = user_list_response.json()

        user_ids = [
            (m["id"], m["name"]) for m in user_list["members"] if not m["is_bot"]
        ]

        user_ids.remove(("USLACKBOT", "slackbot"))

        return user_ids

    def get_available_channels_from_user_id(self, user_id):
        channels_query = "https://slack.com/api/users.conversations"
        parameters = {"user": user_id}

        channels_list_response = requests.get(
            channels_query, params=parameters, headers=self.HEADERS
        )

        channels_list = channels_list_response.json()

        channel_ids = [
            (c["id"], c["name"]) for c in channels_list["channels"] if c["is_channel"]
        ]

        return channel_ids

    def get_last_messages_from_channel(self, channel_id, count=10):
        messages_query = "https://slack.com/api/conversations.history"
        parameters = {"channel": channel_id, "limit": count}

        messages_list_response = requests.get(
            messages_query, params=parameters, headers=self.HEADERS
        )

        messages_list = messages_list_response.json()

        messages_data = [
            c["ts"] for c in messages_list["messages"] if c["type"] == "message"
        ]

        return messages_data

    def get_message_link_from_message(self, channel_id, message_id):
        message_link_query = "https://slack.com/api/chat.getPermalink"
        parameters = {"channel": channel_id, "message_ts": message_id}

        message_link_response = requests.get(
            message_link_query, params=parameters, headers=self.HEADERS
        )

        message_link = message_link_response.json()["permalink"]

        return message_link
