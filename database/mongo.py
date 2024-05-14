# pymongo
from pymongo import MongoClient

# config
from config.config import Config

config = Config()
config = config.config
mongo_client = MongoClient(
    host=config["database"]["mongo"]["host"],
    port=config["database"]["mongo"]["port"],
)
