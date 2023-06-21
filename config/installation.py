from terminalforms import *

import os

form = Form(
    "Installation",
    "Please enter the following information:",

    content=[
        Text("Enter your following access keys."),
        Field("Bot Token"),
        Field("Genius API Key"),

        Text("Enter your following IDs."),
        Field("Your Guild ID"),
        Field("Log Channel ID"),
        Field("Arrival Channel ID"),
        Field("Leave Channel ID"),

        Text("Enter your following colors."),
        Field("Default Embed Color"),
        Field("Default Log Embed Color"),

        Text("Enter your following names."),
        Field("Member Role Name"),
        Field("Ticket Category Name"),

        Text("Enter your following Lavalink node information."),
        Field("Lavalink Node Host"),
        Field("Lavalink Node Port"),
        Field("Lavalink Node Password"),
        Field("Lavalink Node Label"),

        Submit("Submit")
    ]
)

form.show()

path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
with open(f"{path}/config.cfg", "w", encoding="utf-8") as f:
    modal = """{
  "default_guild_id": [[guild_id]],

  "log_channel": [log_channel_id],
  "welcome_channel": [arrival_channel_id],
  "leaving_channel": [leave_channel_id],

  "default_embed_color": "[default_embed_color]",
  "log_embed_color": "[default_log_embed_color]",

  "member_role_name": "[member_role_name]",

  "ticket_category": "[ticket_category_name]",

  "token": "[bot_token]",
  "genius": "[genius_api_key]",

  "node_host": "[lavalink_node_host]",
  "node_port": [lavalink_node_port],
  "node_password": "[lavalink_node_password]",
  "node_label": "[lavalink_node_label]"
}"""

    modal = modal.replace("[guild_id]", form.get("Your Guild ID"))
    modal = modal.replace("[log_channel_id]", form.get("Log Channel ID"))
    modal = modal.replace("[arrival_channel_id]", form.get("Arrival Channel ID"))
    modal = modal.replace("[leave_channel_id]", form.get("Leave Channel ID"))
    modal = modal.replace("[default_embed_color]", form.get("Default Embed Color"))
    modal = modal.replace("[default_log_embed_color]", form.get("Default Log Embed Color"))
    modal = modal.replace("[member_role_name]", form.get("Member Role Name"))
    modal = modal.replace("[ticket_category_name]", form.get("Ticket Category Name"))
    modal = modal.replace("[bot_token]", form.get("Bot Token"))
    modal = modal.replace("[genius_api_key]", form.get("Genius API Key"))
    modal = modal.replace("[lavalink_node_host]", form.get("Lavalink Node Host"))
    modal = modal.replace("[lavalink_node_port]", form.get("Lavalink Node Port"))
    modal = modal.replace("[lavalink_node_password]", form.get("Lavalink Node Password"))
    modal = modal.replace("[lavalink_node_label]", form.get("Lavalink Node Label"))

    f.write(modal)

Text("Installation complete! Press enter to exit...").text()
input()