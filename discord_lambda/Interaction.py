import requests
import time

class Embedding:
    def __init__(self, title: str = "", desc: str = "", url: str = "", color: int = "", fields: list[dict] = [], footer: dict = {}):
        self.title = title
        self.desc = desc
        self.url = url
        self.color = color
        self.fields = fields
        self.footer = footer
    

    def to_dict(self):
        return {
            "title": self.title if self.title else None,
            "description": self.desc if self.desc else None,
            "url": self.url if self.url else None,
            "color": self.color if self.color else None,
            "fields": self.fields if self.fields else None,
            "footer": self.footer if self.footer else None
        }
    

    def set_title(self, title: str):
        self.title = title
    

    def set_description(self, desc: str):
        self.desc = desc


    def set_url(self, url: str):
        self.url = url
    

    def set_color(self, color: int):
        self.color = color
    

    def add_field(self, name: str, value: str, inline: bool):
        # NEVER use append() here 
        self.fields = self.fields + [{"name": name, "value": value, "inline": inline}]
    

    def set_footer(self, text: str, icon_url: str = None):
        self.footer = {"text": text, "icon_url": icon_url}


class Interaction:
    PING_RESPONSE = { "type": 1 }

    def __init__(self, interaction: dict, app_id: str) -> None:
        self.type = interaction.get("type")
        self.token = interaction.get("token")
        self.id = interaction.get("id")
        self.data = interaction.get("data")
        self.callback_url = f"https://discord.com/api/v10/interactions/{self.id}/{self.token}/callback"
        self.webhook_url = f"https://discord.com/api/v10/webhooks/{app_id}/{self.token}/messages/@original"
        self.timestamp = time.time()
    

    def __create_channel_message(self, content: str = None, embeds: list[Embedding] = None, ephemeral: bool = True) -> dict:
        response = {
            "content": content,
            "embeds": [embed.to_dict() for embed in embeds] if embeds else None,
            "flags": 1 << 6 if ephemeral else None
        }
        return response


    def defer(self, ephemeral: bool = True) -> None:
        try:
            requests.post(self.callback_url, json={"type": 5, "data": {"flags": 1 << 6 if ephemeral else None}}).raise_for_status()
        except Exception as e:
            raise Exception(f"Unable to defer response: {e}")
    

    def send_response(self, content: str = None, embeds: list[Embedding] = None, ephemeral: bool = True) -> None:
        try:
            requests.patch(self.webhook_url, json=self.__create_channel_message(content, embeds, ephemeral)).raise_for_status()
        except Exception as e:
            raise Exception(f"Unable to send response: {e}")
    

    def send_followup(self, content: str = None, embeds: list[Embedding] = None, ephemeral: bool = True) -> None:
        try:
            requests.post(self.webhook_url, json=self.__create_channel_message(content, embeds, ephemeral)).raise_for_status()
        except Exception as e:
            raise Exception(f"Unable to send followup: {e}")
