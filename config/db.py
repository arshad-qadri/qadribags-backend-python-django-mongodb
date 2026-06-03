from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()

def connect_db():
    connect(
        host=os.getenv("MONGODB_URI")
    )