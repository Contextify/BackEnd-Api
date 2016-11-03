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
	res=db.location.find(data)
	if list(res):
		return -1
	db.location.insert(data)
	return 0




