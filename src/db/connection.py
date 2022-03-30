import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
DATABASE_URL_CONNECTION = os.getenv("DATABASE_URL_CONNECTION")

try:
    client = MongoClient(DATABASE_URL_CONNECTION)
    db = client.netflexdb
    user_collection = db.users
    dbfilms = db.films
except KeyError:
    client = MongoClient()
    db = client.netflexdb
    user_collection = db.users
    dbfilms = db.films
