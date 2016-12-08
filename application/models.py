import dbtest
import util
from pymongo import MongoClient,errors
from collections import defaultdict,OrderedDict,namedtuple
import config
import json
import numpy as np
statemap={1:"Home",2:"NearHome",3:"Outside",4:"Work",5:"Class",6:"Library"}
reversemap={"Home":1,"NearHome":2,"Outside":3,"Work":4,"Class":5,"Library":6}
# transprob=defaultdict(list,
#     ((1,[0.5,0.5,0,0,0,0]),
#     (2,[0.25,0.25,0.25,0.25,0,0]),
#     (3,[0,0.25,0.25,0,0.25,0.25]),
#     (4,[0,0.5,0,0.5,0,0]),
#     (5,[0,0,0.5,0,0.5,0]),
#     (6,[0,0,0.5,0,0,0.5])
#     ))

def getmax_key(d):
    v=list(d.values())
    k=list(d.keys())
    maxval=max(v)
    maxkey=k[v.index(maxval)]
    return (maxkey,maxval)

class State():
    def __init__(self,name,username):
        self.username=username
        self.name=name

    def getstate():
        res=find()

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
            self.probmax[i]={"State":maxstate,"Prob":max1}
        return self.probmax,self.probdict

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
        b=defaultdict(lambda: defaultdict(dict))
        if day:
            return dayprob[day].getprob()
        for k,v in dayprob.items():
            a[k],b[k]=v.getprob()
        return a,b

    def __repr__(self):
        return self.name

    def get_current_state(self):
        res=list(dbtest.get_current_state(self.name))
        if not res:
            return None
        return {"State":res[0]["State"]}

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


    def calc_prob(self,day=None,state=True):
        res=None
        if day:
            res=dbtest.get_states_by_day(self.name,day)
            res=self._calc_prob(res)
            if state:
                res=self.retdict(res)[0]
            else:
                res=self.retdict(res)[1]
            return res[day]
        else:
            for d in self.days.keys():
                res=dbtest.get_states_by_day(self.name,d)
                res=self._calc_prob(res)
                if state:
                    res=self.retdict(res)[0]
                else:
                    res=self.retdict(res)[1]
            return res

    def lastfewstate(self,limit):
        res=dbtest.last_ten(self.name,limit)
        return list(res)

    def transition_matrix(self):
        trans=defaultdict(lambda: defaultdict(int))
        res=self.get_states()
        for i,j in zip(res,res[1:]):
            if i["State"]!=j["State"]:
                try:
                    trans[i["State"]][j["State"]]+=1
                except:
                    trans[i["State"]][j["State"]]=0
        transprob=defaultdict(lambda: defaultdict(int))
        for k,v in trans.items():
            total=sum(v.values())
            for k1,v1 in v.items():
                transprob[k][k1]=float(v1)/total
        return transprob


    def next_state(self,day=None,hour=0):
        res=None
        next_state_prob={}
        res=self.calc_prob(day,state=False)
        state=self.get_current_state()
        trans=self.transition_matrix()
        currstate=state['State']
        predicted_curr_state=getmax_key(res[hour])[0]
        if predicted_curr_state==currstate:
            currstateprob=res[hour][currstate]
        else:
            currstate,currstateprob=getmax_key(res[hour])
        print currstate,currstateprob
        predstatedict=res[hour]
        predicted_state,predicted_prob_val=getmax_key(predstatedict)
        for i,v in predstatedict.items():
            next_state_prob[i]=float(v)*currstateprob*trans[currstate][i]
        next_state=getmax_key(next_state_prob)
        return {"CurrentState":currstate,"NextState":next_state[0]}
