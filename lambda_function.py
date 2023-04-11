import os
from discord_lambda import InteractionHandler

handler = InteractionHandler(command_dir="commands", app_id=os.environ.get("APP_ID"), public_key=os.environ.get("PUBLIC_KEY"), bot_token=os.environ.get("BOT_TOKEN"))

def lambda_handler(event, context):
    handler.handle(event)

