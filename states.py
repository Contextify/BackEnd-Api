import arrow
import util
import datetime
import dbtest
from collections import defaultdict
days=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
dayobjectmap={}



class DayWise():
	def __init__(self,name):
		self.name=name
		self.time=None
		self.states=[]
		self.timeframe=defaultdict(dict)
		self.probmatrix=defaultdict(dict)
		self.maxprobmap={}

	def set_state(self,state,starttime,endtime):
		if state not in self.states:
			self.states.append(state)
		time=util.toESTHr(starttime)
		try:
			self.timeframe[time][state]+=1
		except KeyError:
			self.timeframe[time][state]=1

	def get_states_by_day(self,user):
		map(self.push_data,dbtest.get_states_by_day(user,self.name))

	def getTimeFrame(self):
		return self.timeframe

	def push_data(self,x):
		self.set_state(x["State"],x["Start"],x["End"])

	def calc_prob(self):
		for time,states in self.timeframe.items():
			totalcount=sum(states.values())
			maxprob=-1
			for state,count in states.items():
				prob=count/float(totalcount)
				self.probmatrix[time][state]=prob
				if prob >= maxprob:
					maxprob=prob
					self.maxprobmap[time]=state
		return self.probmatrix


	
for d in days:
	dayobjectmap[d]=DayWise(d)

def make_state_table(user,dayofWeek):
	day=dayobjectmap[dayofWeek]
	day.get_states_by_day(user)
	yield day.getTimeFrame()

def calc_prob(user,day):
	day=dayobjectmap[day]
	day.get_states_by_day(user)
	return day.calc_prob()

def calc_max_prob(user,day):
	day=dayobjectmap[day]
	day.get_states_by_day(user)
	day.calc_prob()
	return day.maxprobmap

	

