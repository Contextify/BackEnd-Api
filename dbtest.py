from pymongo import MongoClient,errors
import json
import config
import arrow

client = MongoClient('localhost', 27017)
db=client.contextify

def write_location(data):
	loc=db.location
	res=loc.find_one(data)
	print res
	if res:
		print "der\n"
		return -1
	loc.insert(data)
	return 0

