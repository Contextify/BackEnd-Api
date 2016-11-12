from pymongo import MongoClient,errors
client = MongoClient('localhost', 27017)
db=client.test

db.test.insert({"User":"Sriram","time":1})
res=db.test.find()
print list(res)
if res:
	db.test.update({"User":"Sriram","time":1},{"$set":{"time":5}})
print list(db.test.find())
