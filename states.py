import arrow
import util
import datetime
import dbtest
from collections import defaultdict
days=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]





class DayWise():
	def __init__(self,name):
		self.name=name
		self.time=None
		self.states=[]
		self.timeframe=defaultdict(dict)

	def set_state(self,state,starttime):
		if state not in self.states:
			self.states.append(state)
		time=util.getHr(starttime)
		try:
			self.timeframe[time][state]+=1
		except KeyError:
			self.timeframe[time][state]=0

	def getTimeFrame(self):
		return self.timeframe



def make_state_table():
	global days
	dayobjectmap={}
	for d in days:
		dayobjectmap[d]=DayWise(d)
	

