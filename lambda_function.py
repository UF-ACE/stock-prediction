import os
from nacl.signing import VerifyKey
from discord_lambda import Interaction, Embedding
import pickle


def verify_signature(event: dict) -> None:
    raw_body = event.get("rawBody")
    auth_sig = event['params']['header'].get('x-signature-ed25519')
    auth_ts  = event['params']['header'].get('x-signature-timestamp')

    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(os.environ.get('PUBLIC_KEY')))
    verify_key.verify(message, bytes.fromhex(auth_sig))


def lambda_handler(event, context):
    try:
        verify_signature(event)
    except Exception as e:
        # Return a 401 Unauthorized response
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")
    
    interaction = Interaction(event.get("body-json"), os.environ.get('APP_ID'))

    if interaction.type == 1:
        return Interaction.PING_RESPONSE
    
    elif interaction.type == 2:
        interaction.defer(ephemeral=True)

        registry = pickle.load(open("/opt/CommandRegistry.pickle", "rb"))
        try:
            func, args = registry.find_func(interaction.data)
            func(interaction, **args)
        except Exception as e:
            interaction.send_response(embeds=[Embedding(":x: Error", f"The request could not be completed:\n`{e}`", color=0xFF0000)])