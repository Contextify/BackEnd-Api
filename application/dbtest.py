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
	st=db.state
	res=loc.find_one(data)
	curr_state=st.find_one({"User":data["User"]})
	print curr_state
	if curr_state:
		st.update({"_id":ObjectId(curr_state["_id"])},{"$set":{"State":data["State"]}})
	else:
		st.insert({"User":data["User"],"State":data["State"]})

	if res:
		return -1
	loc.insert(data)
	return 0

def update_prev_state(data):
	loc=db.location
	d={"User":data['User'],"Start":data["Laststatetime"],"State":data["Laststate"],"End":"None"}
	res=loc.find_one(d)
	if res:
		loc.update(d,{"$set":{"End":data["Timestamp"],"Enddate":arrow.get(data["Timestamp"]).to("utc").datetime}},False,True)


def last_ten(user,limit):
	loc=db.location
	return loc.find({"User":user},{"_id":0,"Startdate":0,"Enddate":0,"User":0}).sort([("Start",-1)]).limit(limit)

def get_current_state(user):
	statedb=db.state
	return list(statedb.find({"User":user}))

def get_states_by_day(user,day=None,state=None):
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
	try:
		return list(res["result"])
	except TypeError:
		return list(res)
