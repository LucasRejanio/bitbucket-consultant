from pymongo import MongoClient
import os

class MongoDBConn():
  def __init__(self, database: str):
    user = os.getenv("MONGODB_USER")
    pswd = os.getenv("MONGODB_PASSWORD")
    host = os.getenv("MONGODB_HOST")
    port = int(os.getenv("MONGODB_PORT"))
    client = MongoClient(f"mongodb://{user}:{pswd}@{host}:{port}/")
    self.db = client[database]

  def find_by_id(self, collection: str, id: any):
    return self.db[collection].find_one({"_id": id})

  def find(self, collection: str, filter: dict, project:dict=None):
    res = []
    cursor = self.db[collection].find(filter, project)
    for r in cursor:
      res.append(r)
    return res

  def find_one(self, collection: str):
    return self.db[collection].find_one()

  def insert_one(self, collection: str, item: dict):
    return self.db[collection].insert_one(item)

  def insert_many(self, collection: str, items: dict):
    return self.db[collection].insert_many(items)

  def replace_one(self, collection: str, filter: dict, item: dict):
    return self.db[collection].replace_one(filter, item)

  def drop_collection(self, collection: str):
    return self.db.drop_collection(collection)
