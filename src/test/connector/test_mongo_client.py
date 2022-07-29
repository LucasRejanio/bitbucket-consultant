from pymongo.database import Database
from connector.mongo_client import MongoDBConn
from test.connector.mongodb_decorator import clear_prev_test, generate_item, generate_items
from dotenv import load_dotenv

load_dotenv()

conn = MongoDBConn(database="test")

# Tests
def test_mongodb_class_compatibility():
  assert type(conn.db) is Database

@clear_prev_test
def test_mongodb_find_by_id():
  item = generate_item()
  conn.insert_one(collection="coll", item=item)
  inserted = conn.find_by_id(collection="coll", id=item["_id"])
  assert inserted == item

@clear_prev_test
def test_mongodb_find():
  items = generate_items()
  conn.insert_many(collection="coll", items=items)
  result = conn.find(collection="coll", filter={"this": "some_text"})
  assert len(result) == len(items)
  assert result == items

@clear_prev_test
def test_mongodb_insert_one_always_return_id():
  id = conn.insert_one(collection="coll", item=generate_item())
  assert id is not None

@clear_prev_test
def test_mongodb_replace_one():
  old = generate_item()
  new = old
  new["_id"] = old["_id"]
  id = conn.insert_one(collection="coll", item=old)
  conn.replace_one(collection="coll", filter={"_id": old["_id"]}, item=new)
  replaced = conn.find_by_id(collection="coll", id=old["_id"])
  assert replaced["_id"] == old["_id"]
  assert replaced == new