import os
import pickle
from .CommandRegistry import CommandRegistry

registry = CommandRegistry(command_dir="commands", app_id=os.environ.get('APP_ID'), bot_token=os.environ.get('BOT_TOKEN'))

with open("CommandRegistry.pickle", "wb") as f:
    pickle.dump(registry, f, protocol=pickle.HIGHEST_PROTOCOL)