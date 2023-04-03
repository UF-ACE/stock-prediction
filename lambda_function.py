import os
from nacl.signing import VerifyKey
from utils import Interaction

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")


def verify_signature(event):
    raw_body = event.get("rawBody")
    auth_sig = event['params']['header'].get('x-signature-ed25519')
    auth_ts  = event['params']['header'].get('x-signature-timestamp')
    
    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig)) 


def lambda_handler(event, context):
    # Verify the signature
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")
    
    # Create an Interaction object and respond to the request
    inter = Interaction(event.get("body-json"))
    inter.respond()

   