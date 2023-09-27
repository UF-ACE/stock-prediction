import pickle


def lambda_handler(event, context):
    handler = pickle.load(open("/opt/InteractionHandler.pickle", "rb"))
    handler.handle(event)