import arrow

def toEST(UTCtimestamp):
	return arrow.get(UTCtimestamp).to("US/Eastern").timestamp

def getDay(UTCtimestamp):
	return arrow.get(UTCtimestamp).format("dddd")