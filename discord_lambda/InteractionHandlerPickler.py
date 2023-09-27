import os
import pickle
from .InteractionHandler import InteractionHandler

handler = InteractionHandler(command_dir="commands", app_id=os.environ.get('APP_ID'), public_key=os.environ.get('PUBLIC_KEY'), bot_token=os.environ.get('BOT_TOKEN'))

with open("InteractionHandler.pickle", "wb") as f:
    pickle.dump(handler, f, protocol=pickle.HIGHEST_PROTOCOL)