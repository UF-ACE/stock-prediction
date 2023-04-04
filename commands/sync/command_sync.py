import requests
import json
import os

APP_ID = os.environ.get("APP_ID")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
url = f"https://discord.com/api/v10/applications/{APP_ID}/commands"
headers = {
    "Authorization": f"Bot {BOT_TOKEN}"
}

def main():
    with open("commands/sync/commands.json") as f:
        data = json.load(f)
        for x in data:
            requests.post(url, json=x, headers=headers).raise_for_status()

    print("Successfully synced commands.")

if __name__ == "__main__":
    main()