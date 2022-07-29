from random import randint

from connector.mongo_client import MongoDBConn

def clear_prev_test(funct):
  def clear():
    conn = MongoDBConn(database="test")
    conn.drop_collection(collection="coll")
    funct()
  return clear

def generate_item():
  return {"_id":randint(1, 9999), "this": "some_text"}

def generate_items():
  items = []
  for i in range(0,10):
    item = {
      "_id": randint(1, 9999),
      "this": "some_text"
    }
    items.append(item)
  return items