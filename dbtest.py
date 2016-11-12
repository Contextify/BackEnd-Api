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
	d={"User":data['User'],"State":data["Laststate"],"End":"None","Start":data["Laststatetime"]}
	res=loc.find_one(d)
	if res:
		loc.update(d,{"$set":{"End":data["Timestamp"]}},False,True)

def get_states(user):
	loc=db.location
	print user
	res=loc.find({"User":user})
	return list(res)



def make_table(user):
	res=get_states(user)
	for i in res:
		print i

make_table("Sriram")