import dbtest
import util
from pymongo import MongoClient,errors
from collections import defaultdict,OrderedDict,namedtuple
import config

# def daytoHr(day,)
class User():
    def __init__(self,name):
        self.name=name.title()
        self.days={1:"Sunday",2:"Monday",3:"Tuesday",4:"Wednesday",5:"Thursday",6:"Friday",7:"Saturday"}
        self.dbclient = MongoClient('localhost', 27017)
        self.db=self.dbclient.contextify
        self.dayprob=defaultdict(dict)

    def __repr__(self):
        return self.name

    def get_states(self,start=None,end=None):
        loc=self.db.location
        if start and end:
            res=loc.find({"User":self.name,"Start":{"$gt":start,"$lt":end}})
        elif start and end==None:
            res=loc.find({"User":self.name,"Start":{"$gt":start}})
        else:
            res=loc.find({"User":self.name})
        return list(res)

    def get_states_percent(self):
        statecount=[]
        totalcount=self.db.location.find({"User":self.name}).count()
        for state in config.states:
            d={}
            d["State"]=state
            d["Count"]=self.db.location.find({"User":self.name,"State":state}).count()
            d["Percent"]=d["Count"]*100/float(totalcount)
            statecount.append(d)
        return statecount

    def getStatesByDay(self,day=None):
        if not day:
            for day in self.days.values():
                res=dbtest.get_states_by_day(self.name,day)
                self.dayprob[day]=res
            return self.dayprob
        res=dbtest.get_states_by_day(self.name,day)
        self.dayprob[day]=res
        return self.dayprob

    def calc_prob(self,day=None):
        if not day:
            for d in self.days.values():
                hrdict=defaultdict(list)
                res=self.getStatesByDay(d)
            return res
        return self.getStatesByDay(day)
