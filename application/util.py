import arrow

from config import Timezone

def getHostname():
	import socket
	return socket.gethostname()

def toEST(UTCtimestamp):
	return arrow.get(UTCtimestamp).to("US/Eastern").timestamp

def toESTHr(UTCtimestamp):
	return arrow.get(UTCtimestamp).to("US/Eastern").format("HH")

def toESTday(UTCtimestamp):
	return arrow.get(UTCtimestamp).to("US/Eastern").format("dddd")
	
def getDay(timestamp):
	return arrow.get(timestamp).format("dddd")

def getHr(timestamp):
	return arrow.get(timestamp).format("HH")

def getdatetime(timestamp):
	return arrow.get(timestamp).to("US/Eastern").datetime

def timerange(start,end):
	start=getdatetime(start)
	end=getdatetime(end)
	return arrow.Arrow.span_range('hour', start, end)
def gettimeresp(res):
	data=[]
	for i in res:
		start=int(toEST(i['Start']))
		startdate=getdatetime(start)
		start*=1000
		if i["End"]!="None":
			end=int(toEST(i['End']))
			enddate=getdatetime(end)
			end*=1000
		else:
			enddate=arrow.now().datetime
			end=int(toEST(arrow.now().timestamp)*1000)
		a={"content":i['State'],"start":start,"end":end}
		data.append(a)
		data.sort(key=lambda x:x['start'])
	return data
