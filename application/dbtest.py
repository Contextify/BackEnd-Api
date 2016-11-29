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
	loc.insert(data)
	return 0

def update_prev_state(data):
	loc=db.location
	d={"User":data['User'],"State":data["Laststate"],"End":"None"}
	res=loc.find_one(d)
	if res:
		loc.update(d,{"$set":{"End":arrow.get(data["Timestamp"]).to("utc").timestamp,"Enddate":arrow.get(data["Timestamp"]).to("utc").datetime}},False,True)


def get_states_by_day(user,day=None):
	if user==None or day==None:
		return -1
	day=day.title()
	days={"Sunday":1,"Monday":2,"Tuesday":3,"Wednesday":4,"Thursday":5,"Friday":6,"Saturday":7}
	loc=db.location
	s=days[day]
	pipe=[
	{
		"$project": {
			"_id":0,
			"User":"$User",
			"Starthour":{"$hour":"$Startdate"},
			"dow": { "$dayOfWeek": "$Startdate" },
			"State":"$State",
			"Start":"$Start",
			"End":"$End",
		}
	},
	{
		"$match": {"User":user,"dow":s}
	}
	]
	res=loc.aggregate(pipeline=pipe)
	return list(res)
