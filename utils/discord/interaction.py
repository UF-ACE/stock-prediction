import requests
import time
import os
from utils.discord import Embedding
from utils import send_embed
from commands import sentiment, help

APP_ID = os.environ.get("APP_ID")


class Interaction:
    def __init__(self, interaction: dict) -> None:
        self.type = interaction.get("type")
        self.token = interaction.get("token")
        self.id = interaction.get("id")
        self.data = interaction.get("data")
        self.callback_url = f"https://discord.com/api/v10/interactions/{self.id}/{self.token}/callback"
        self.webhook_url = f"https://discord.com/api/v10/webhooks/{APP_ID}/{self.token}/messages/@original"
        self.timestamp = time.time()
    
    def respond(self) -> None:
        # Pong response
        if self.type == 1:
            requests.post(self.callback_url, json={"type": 1})
        
        # Command response
        elif self.type == 2:
            # Send the loading message
            requests.post(self.callback_url, json={"type": 5})

            # Start constructing the response
            embed = None
            try:
                # Get the command name and options
                name = self.data.get("name")
                options = self.data.get("options")

                if name == "sentiment":
                    embed = sentiment(options)

                elif name == "help":
                    embed = help(options)
                
                # Add the footer and send
                embed.set_footer(f"Request completed in {round(time.time() - self.timestamp, 2)}s\n" \
                                 "Bot is running version 1.0.0")    # TODO: sync this with GitHub releases
                send_embed(embed, self.webhook_url)

            except Exception as e:
                # Send an error message
                embed = Embedding(":x:  Error", "The request could not be completed at this time.\n" \
                        "If this issue persists, please submit an issue on [GitHub](https://github.com/UF-ACE/stock-prediction).\n", 
                        color=0xFF0000)
                send_embed(embed)
                raise Exception(f"[ERROR] {e}")