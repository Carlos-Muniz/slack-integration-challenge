import os
from random import choice
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_web_api import slack_web_api
from behind_the_name_api import behind_the_name_api

# gets bot token
BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
NAME_API_KEY = os.environ.get("NAME_API_KEY")

# Initializes your app with your bot token and socket mode handler
app = App(token=BOT_TOKEN)


def get_random_element(array):
    return choice(array)


@app.command("/randomx2")
def post_doubly_random_messages(ack, respond):
    ack()
    slack = slack_web_api(BOT_TOKEN)
    user_data = slack.get_available_user_ids()
    user_id, user_name = get_random_element(user_data)
    channel_data = slack.get_available_channels_from_user_id(user_id)
    channel_id, channel_name = get_random_element(channel_data)
    messages = slack.get_last_messages_from_channel(channel_id)
    message_links = [
        slack.get_message_link_from_message(channel_id, m) for m in messages
    ]
    text = (
        f"Here are up to 10 messages picked from @{user_name}'s " +
        f"membership to #{channel_name}:\n" +
        "\n".join([f"{i:02d}) {m}" for i, m in enumerate(message_links, 1)])
    )
    respond(text)


@app.command("/relatednames")
def post_related_names(ack, respond, command):
    ack()
    btn = behind_the_name_api(NAME_API_KEY)
    name = command["text"]
    related_names = btn.get_related_names(name)
    text = f"Here is a list of names related to {name}:\n" + "\n".join(
        [f"{i:02d}) {n}" for i, n in enumerate(related_names, 1)]
    )
    respond(text)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
