import arrow

def toEST(UTCtimestamp):
	return arrow.get(UTCtimestamp).to("US/Eastern").timestamp