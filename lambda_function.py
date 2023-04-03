import requests
import os
from nacl.signing import VerifyKey
from commands import sentiment, help

PUBLIC_KEY = os.environ.get("PUBLIC_KEY")
APP_ID = os.environ.get("APP_ID")

PONG = {
    "type": 1
}
LOADING = {
    "type": 5
}
ERROR = {
    "embeds": [
        {
            "title": ":x: Error",
            "description": "The request could not be completed at this time.\nIf this issue persists, please submit an issue on [GitHub](https://github.com/UF-ACE/stock-prediction).",
            "color": 0xFF0000,
        }
    ]
}


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
    
    # Get the request body and the type
    body = event.get('body-json')
    type = body.get("type")

    # Check if message is a ping
    if type == 1:
        return PONG # the ONLY time we return a response -> everything else is async
    
    # Get general info from the request body
    token = body.get("token")
    id = body.get("id")
    
    # Is the message a command?
    if type == 2:
        url = f"https://discord.com/api/v10/interactions/{id}/{token}/callback"
        try:
            # Send a loading message
            requests.post(url, json=LOADING)

            # Start constructing the response
            url = f"https://discord.com/api/v10/webhooks/{APP_ID}/{token}/messages/@original"
            json = {}

            # Get the command name and options
            name = body.get("data").get("name")
            options = body.get("data").get("options")

            if name == "sentiment":
                json = sentiment(options)

            elif name == "help":
                json = help(options)
            
            else:
                raise Exception("Unknown command.")

            # Send the response
            requests.patch(url, json=json)

        except Exception as e:
            # Send an error message
            requests.patch(url, json=ERROR)
            raise Exception(f"[ERROR] {e}")
    
    else:
        raise Exception("Unsupported request type.")


   