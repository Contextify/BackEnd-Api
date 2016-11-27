from flask import Flask,render_template,jsonify,request,Response
import json
import arrow
import util
import models
app = Flask(__name__)

@app.route("/")
def id():
	return "Contextify Homepage"

@app.route("/user/<user>")
def index(user):
	s=models.User(user)
	res=s.get_states_by_day()
	data=util.gettimeresp(res)
	return jsonify(data)

if __name__=="__main__":
	app.run(host="0.0.0.0",port=4000)
