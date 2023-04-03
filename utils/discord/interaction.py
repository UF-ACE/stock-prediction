import requests
import time
import os
from utils.discord import Embedding
from commands import sentiment, help

APP_ID = os.environ.get("APP_ID")

class Interaction:
    ERROR = Embedding(":x: Error", "The request could not be completed at this time.\
                      \nIf this issue persists, please submit an issue on [GitHub](https://github.com/UF-ACE/stock-prediction).", color=0xFF0000)
    
    def __init__(self, interaction: dict):
        self.type = interaction.get("type")
        self.token = interaction.get("token")
        self.id = interaction.get("id")
        self.data = interaction.get("data")
        self.callback_url = f"https://discord.com/api/v10/interactions/{self.id}/{self.token}/callback"
        self.webhook_url = f"https://discord.com/api/v10/webhooks/{APP_ID}/{self.token}/messages/@original"
        self.timestamp = time.time()
    
    def send_embed(self, embed: Embedding):
        if not embed.footer:
            embed.set_footer(f"Request completed in {round(time.time() - self.timestamp, 2)}s")
        requests.patch(self.webhook_url, json={"embeds": [embed.to_dict()]})
    
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
                self.send_embed(self.ERROR)
                raise Exception(f"[ERROR] {e}")