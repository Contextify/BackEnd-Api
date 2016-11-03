from flask import Flask,render_template,make_response
app = Flask(__name__)
import json
from DbHandler import get_states
@app.route("/")
def index():
    res=list(get_states())
    return json.dumps(res,indent=4,sort_keys=True)
    
@app.route("/timeline")
def tm():
    print "Timeline requested"
    return app.send_static_file('timeline.html')
   
if __name__=="__main__":
	app.run(host="0.0.0.0",port=4000)
