
from util import getDay

class State():
	def __init__(self,name,start,end):
		self.name=name
		self.start=start
		self.end=end
		self.startday=None
		self.endday=None

	def get_day(self):
		self.startday=getDay(self.start)
		self.endday=getDay(self.end)
		return self.startday




