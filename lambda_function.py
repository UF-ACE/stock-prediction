import pickle

def lambda_handler(event, context):
    handler = pickle.load(open("InteractionHandler.pickle", "rb"))
    handler.handle(event)