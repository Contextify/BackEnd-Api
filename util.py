import arrow

def toEST(UTCtimestamp):
	return arrow.get(UTCtimestamp).to("US/Eastern").timestamp

def toESTHr(UTCtimestamp):
	return arrow.get(UTCtimestamp).to("US/Eastern").format("HH")
	
def getDay(timestamp):
	return arrow.get(timestamp).format("dddd")

def getHr(timestamp):
	return arrow.get(timestamp).format("HH")

def gettimeresp(res):
	data=[]
	for i in res:
		start=int(toEST(i['Start']))*1000
		if i["End"]!="None":
			end=int(toEST(i['End']))*1000	
		else:
			end=int(toEST(arrow.now().timestamp)*1000)
		a={"content":i['State'],"start":start,"end":end}
		data.append(a)
	return data
