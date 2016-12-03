import dbtest
import util
from pymongo import MongoClient,errors
from collections import defaultdict,OrderedDict,namedtuple
import config
import json

statemap={1:"Home",2:"NearHome",3:"Outside",4:"Work",5:"Class",6:"Library"}
transprob=defaultdict(list,
    ((1,[0,1,0,0,0,0]),
    (2,[0.33,0,0.33,0.33,0,0]),
    (3,[0,0.33,0,0,0.33,0.33]),
    (4,[0,1,0,0,0,0]),
    (5,[0,0,1,0,0,0]),
    (6,[0,0,1,0,0,0])
    ))

class Day():
    def __init__(self,name):
        self.name=name
        self.hourdict=defaultdict(dict)
        self.d={}
        self.probdict=defaultdict(dict)
        self.probmax={}
    def addcount(self,hour,state):
        try:
            self.hourdict[int(hour)][state]+=1
        except KeyError:
            self.hourdict[int(hour)][state]=1

    def getcount(self):
        return self.hourdict

    def getprob(self):
        for i,v in self.hourdict.items():
            total=sum(v.values())
            max1=0
            maxstate=None
            for k,v1 in v.items():
                prob=v1/float(total)
                self.probdict[i][k]=prob
                if max1<prob:
                    maxstate=k
                    max1=prob
            self.probmax[i]=maxstate
        return self.probmax
        
class User():
    def __init__(self,name):
        self.name=name.title()
        self.days={"Sunday":1,"Monday":2,"Tuesday":3,"Wednesday":4,"Thursday":5,"Friday":6,"Saturday":7}
        self.dbclient = MongoClient('localhost', 27017)
        self.db=self.dbclient.contextify
        self.dayprob={}
        for d in self.days.keys():
            self.dayprob[d]=Day(d)

    def retdict(self,dayprob,day=None):
        a=defaultdict(lambda: defaultdict(dict))
        if not day:
            for k,v in dayprob.items():
                a[k]=v.getprob()
            return a
        return dayprob[day].getprob()

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

    def _calc_prob(self,res):
        for i in res:
            if i["End"]=="None":
                continue
            for d,_ in util.timerange(i["Start"],i["End"]):
                day=util.toESTday(d.timestamp)
                hr=util.toESTHr(d.timestamp)
                state=i["State"]
                self.dayprob[day].addcount(hr,state)
        return self.dayprob


    def calc_prob(self,day=None):
        res=None
        if day:
            res=dbtest.get_states_by_day(self.name,day)
            res=self._calc_prob(res)
            res=self.retdict(res)
            return {day:res[day]}
        else:
            for d in self.days.keys():
                res=dbtest.get_states_by_day(self.name,d)
                print res
                res=self._calc_prob(res)
                res=self.retdict(res)
            return res
