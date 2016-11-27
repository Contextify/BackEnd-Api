from flask import Flask,render_template,jsonify,request,Response
from flask_restful import Resource,Api
import json
import arrow
import util
import models


app = Flask(__name__)
api = Api(app)
class HelloWorld(Resource):
    def get(self):
        return "Contextify Backend API"

class UserData(Resource):
	def get(self,username):
		user=models.User(username)
		res=util.gettimeresp(user.get_states())
		return jsonify(res)

class UserDatabyDay(Resource):
	def get(self,username,day):
		user=models.User(username)
		res=user.get_states_by_day(day)
		return jsonify(res)

api.add_resource(HelloWorld, '/')
api.add_resource(UserData,"/user/<string:username>")
api.add_resource(UserDatabyDay,"/user/<string:username>/<string:day>")

if __name__=="__main__":
	app.run(host="0.0.0.0",port=4000)
