from pymongo import MongoClient

def drop_db():
  client = MongoClient('mongodb://localhost:27017/')
  client.drop_database('EPLLeague')
  print("Database dropped")

drop_db()
