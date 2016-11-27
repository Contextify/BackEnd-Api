from flask import Flask,render_template,jsonify,request,Response
from flask_restful import Resource,Api,reqparse
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
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=int)
        parser.add_argument('end', type=int)
        args = parser.parse_args()
        start = args.get('start')
        end=args.get('end')
        user=models.User(username)
        res=util.gettimeresp(user.get_states(start,end))
        return jsonify(res)

class UserProb(Resource):
    def get(self,username):
        parser = reqparse.RequestParser()
        parser.add_argument('day', type=str)
        args = parser.parse_args()
        day = args.get('day')
        user=models.User(username)
        res=user.calc_prob(day)
        return jsonify(res)

api.add_resource(HelloWorld, '/')
api.add_resource(UserData,"/user/<string:username>")
# api.add_resource(UserDatabyDay,"/user/<string:username>/day")
api.add_resource(UserProb,"/user/<string:username>/prob")

if __name__=="__main__":
	app.run(host="0.0.0.0",port=4000)
