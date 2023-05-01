from .CommandRegistry import CommandRegistry
from .Interaction import Interaction
from nacl.signing import VerifyKey
import requests


class InteractionHandler:
    def __init__(self, command_dir: str, app_id: str, public_key: str, bot_token: str) -> None:
        self.app_id = app_id
        self.public_key = public_key
        self.registry = CommandRegistry(command_dir, app_id, bot_token)


    def __verify_signature(self, event: dict) -> None:
        raw_body = event.get("rawBody")
        auth_sig = event['params']['header'].get('x-signature-ed25519')
        auth_ts  = event['params']['header'].get('x-signature-timestamp')
    
        message = auth_ts.encode() + raw_body.encode()
        verify_key = VerifyKey(bytes.fromhex(self.public_key))
        verify_key.verify(message, bytes.fromhex(auth_sig))
    

    def handle(self, event: dict) -> None:
        try:
            self.__verify_signature(event)
        except Exception as e:
            # Return a 401 Unauthorized response
            raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")
        
        interaction = Interaction(event.get("body-json"), self.app_id)
        if interaction.type == 1:   # Ping
            requests.post(interaction.callback_url, json={"type": 1})
            return
        
        elif interaction.type == 2:   # Slash command
            requests.post(interaction.callback_url, json={"type": 5, "data": {"flags": 1 << 6}})

            # Handle command
            func, args = self.registry.find_func(interaction.data)
            func(interaction, **args)


            
            
        

