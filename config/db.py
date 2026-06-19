import os

from dotenv import load_dotenv
from mongoengine import connect
from mongoengine.connection import get_connection

load_dotenv()


def connect_db():
    try:
        get_connection()
        return
    except Exception:
        pass

    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        raise RuntimeError("MONGODB_URI environment variable is not set.")

    connect(host=mongo_uri)
