from pymongo import MongoClient,errors
import json
import config
import arrow


def get_db():
    client = MongoClient('localhost:27017')
    db = client.contextify
    return db


def write_loc(data):
	db=get_db()
	print data
	res=db.location.find({"user":data['User'],"time":data['Timestamp']})
	if len(list(res)):
		print True