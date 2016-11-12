from flask import Flask,render_template,jsonify,Request,Response
import json
import arrow
import dbtest
from util import toEST
app = Flask(__name__)


@app.route("/user/<user>")
def index(user):
    res=dbtest.get_states(user.title())
    data=[]
    for i in res:
    	start=int(toEST(i['Start']))*1000
    	if i["End"]!="None":
    		end=int(toEST(i['End']))*1000	
    	else:
    		end=int(toEST(arrow.now().timestamp)*1000)
    	a={"content":i['State'],"start":start,"end":end}
    	data.append(a)
    return jsonify(data)
    
@app.route("/timeline")
def tm():
    print "Timeline requested"
    return app.send_static_file('timeline.html')
   
if __name__=="__main__":
	app.run(host="0.0.0.0",port=4000)
