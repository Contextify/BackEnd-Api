import dbtest
import util

class User():
    def __init__(self,name):
        self.name=name.title()
        self.days={1:"Sunday",2:"Monday",3:"Tuesday",4:"Wednesday",5:"Thursday",6:"Friday",7:"Saturday"}

    def __repr__(self):
        return self.name

    def get_states(self):
    	loc=dbtest.db.location
    	res=loc.find({"User":self.name})
        return list(res)

    def get_states_by_day(self,day=None):
    	days={"Sunday":1,"Monday":2,"Tuesday":3,"Wednesday":4,"Thursday":5,"Friday":6,"Saturday":7}
    	loc=db.location
    	s=days[day]
    	pipe=[
    	{
    	    "$project": {
    	        "dow": { "$dayOfWeek": "$Startdate" },
    	        "State":"$State",
    	        "User":"$User",
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
