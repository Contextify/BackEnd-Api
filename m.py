from pymongo import MongoClient,errors
import arrow

client = MongoClient('localhost', 27017)
db=client.contextify
yest=arrow.utcnow().replace(hours=-24).timestamp
print list(db.location.find({"Start":{"$gt":yest}}))