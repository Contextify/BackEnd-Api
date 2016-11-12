from pymongo import MongoClient,errors
from bson.objectid import ObjectId
import json
import config
import arrow

client = MongoClient('localhost', 27017)
db=client.contextify

def write_location(data):
	loc=db.location
	res=loc.find_one(data)
	if res:
		return -1
	loc.insert(data)
	return 0

def update_prev_state(data):
	loc=db.location
	res=loc.find_one({"User":data['User'],"State":data["Laststate"],"End":"None","Start":data["Laststatetime"]})
	if res:
		loc.update({"_id":res["_id"]},{"End":data['Timestamp']})

def get_states(user):
	loc=db.location
	print user
	res=loc.find({"User":user})
	return list(res)
