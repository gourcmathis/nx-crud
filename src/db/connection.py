import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
DATABASE_URL_CONNECTION = os.getenv("DATABASE_URL_CONNECTION")

try:
    client = MongoClient(DATABASE_URL_CONNECTION)
    db = client.netflexdb
    dbusers = db.users
except KeyError:
    client = MongoClient()
    db = client.netflexdb
    dbusers = db.users