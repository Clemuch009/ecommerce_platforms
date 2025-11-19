from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
r = client.admin.command('ping')
print(r)
