import dbtest
import util
from pymongo import MongoClient,errors
from collections import defaultdict,OrderedDict

class User():
    def __init__(self,name):
        self.name=name.title()
        self.days={1:"Sunday",2:"Monday",3:"Tuesday",4:"Wednesday",5:"Thursday",6:"Friday",7:"Saturday"}
        self.dbclient = MongoClient('localhost', 27017)
        self.db=self.dbclient.contextify
        self.dayprob=defaultdict(dict)

    def __repr__(self):
        return self.name

    def get_states(self):
    	loc=self.db.location
    	res=loc.find({"User":self.name})
        return list(res)

    def get_states_by_day(self,day=None):
        if day:
            day=day.title()
    	days={"Sunday":1,"Monday":2,"Tuesday":3,"Wednesday":4,"Thursday":5,"Friday":6,"Saturday":7}
    	loc=self.db.location
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
    	    "$match": {"User":self.name,"dow":s}
    	}
    	]
    	res=loc.aggregate(pipeline=pipe)
        return res["result"]

    def calc_prob(self,day=None):
        if not day:
            for day in self.days.values():
                res=self.get_states_by_day(day)
                self.dayprob[day]=res
            return self.dayprob

        res=self.get_states_by_day(day)
        self.dayprob[day]=res
        return self.dayprob
