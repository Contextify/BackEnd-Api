from flask import Flask,render_template,jsonify,request,Response
import json
import arrow
import dbtest
import util
import states
app = Flask(__name__)

@app.route("/")
def id():
	return "Contextify Homepage"


@app.route("/user/<user>")
def index(user):
	res=dbtest.get_states(user.title())
	data=util.gettimeresp(res)
	return jsonify(data)
    
@app.route("/timeline",methods=['GET', 'POST'])
def tm():
    print "Timeline requested"
    username = request.form['user']
    print(username)
    return app.send_static_file('timeline.html')


if __name__=="__main__":
	app.run(host="0.0.0.0",port=4000)
