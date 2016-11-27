from pymongo import MongoClient,errors
from bson.objectid import ObjectId
import json
import config
import arrow
import util
from collections import defaultdict
import os

client = MongoClient('localhost', 27017)
db=client.contextify

def write_location(data):
	loc=db.location
	res=loc.find_one(data)
	if res:
		return -1
	db.states.insert({"Current":data["State"]})
	loc.insert(data)
	return 0

def update_prev_state(data):
	loc=db.location
	d={"User":data['User'],"End":"None"}
	res=loc.find_one(d)
	if res:
		loc.update(d,{"$set":{"End":arrow.get(data["Timestamp"]).to("utc").timestamp,"Enddate":arrow.get(data["Timestamp"]).to("utc").datetime}},False,True)
