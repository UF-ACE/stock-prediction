import requests
import os
from commands import sentiment, help
import time

APP_ID = os.environ.get("APP_ID")


class Embedding:
    def __init__(self, title: str = "", description: str = "", url: str = "", color: int = "", fields: list = [], footer: dict = {}):
        self.title = title
        self.description = description
        self.url = url
        self.color = color
        self.fields = fields
        self.footer = footer
    
    def to_dict(self):
        return {
            "title": self.title if self.title else None,
            "description": self.description if self.description else None,
            "url": self.url if self.url else None,
            "color": self.color if self.color else None,
            "fields": self.fields if self.fields else None,
            "footer": self.footer if self.footer else None
        }
    
    def set_title(self, title: str):
        self.title = title
    
    def set_description(self, description: str):
        self.description = description

    def set_url(self, url: str):
        self.url = url
    
    def set_color(self, color: int):
        self.color = color
    
    def add_field(self, name: str, value: str, inline: bool):
        self.fields.append({"name": name, "value": value, "inline": inline})
    
    def set_footer(self, text: str, icon_url: str = "https://uf-ace.com/static/media/logo-min.1380c5e0.png"):
        self.footer = {"text": text, "icon_url": icon_url}


class Interaction:
    ERROR = Embedding(":x: Error", "The request could not be completed at this time.\
                      \nIf this issue persists, please submit an issue on [GitHub](https://github.com/UF-ACE/stock-prediction).", color=0xFF0000)
    
    def __init__(self, interaction: dict):
        self.type = interaction.get("type")
        self.token = interaction.get("token")
        self.id = interaction.get("id")
        self.data = interaction.get("data")
        self.callback_url = f"https://discord.com/api/v10/interactions/{self.id}/{self.token}/callback"
        self.webhook_url = f"https://discord.com/api/v10/webhooks/{APP_ID}/{self.token}"
        self.timestamp = time.time()
    
    def send_embed(self, embed: Embedding):
        if not embed.footer:
            embed.set_footer(f"Request completed in {round(time.time() - self.timestamp, 2)}s")
        requests.patch(self.webhook_url, json=embed.to_dict())
    
    def respond(self):
        # Pong response
        if self.type == 1:
            requests.post(self.callback_url, json={"type": 1})
        
        # Command response
        elif self.type == 2:
            # Send the loading message
            requests.post(self.callback_url, json={"type": 5})

            # Start constructing the response
            try:
                # Get the command name and options
                name = self.data.get("name")
                options = self.data.get("options")

                if name == "sentiment":
                    self.send_embed(sentiment(options))

                elif name == "help":
                    self.send_embed(help(options))

            except Exception as e:
                # Send an error message
                requests.patch(self.webhook_url, json=self.ERROR.to_dict())
                raise Exception(f"[ERROR] {e}")


# Given a company name, return the corresponding ticker
def get_ticker(query: str) -> str:
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": query, "quotes_count": 0, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
    data = res.json()
    try:
        return data['quotes'][0]['symbol']
    except Exception as e:
        raise Exception("Invalid company name.")