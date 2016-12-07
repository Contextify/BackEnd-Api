from flask import Flask,render_template,jsonify,request,Response,url_for,make_response
from flask_restful import Resource,Api,reqparse
from flask_cors import CORS, cross_origin
import json
import arrow
import util
import models
app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/user/*": {"origins": "*"}})

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

class StatePercent(Resource):
    def get(self,username):
        user=models.User(username)
        return jsonify(user.get_states_percent())

class UserProb(Resource):
    def get(self,username):
        parser = reqparse.RequestParser()
        parser.add_argument('day', type=str)
        args = parser.parse_args()
        day = args.get('day')
        user=models.User(username)
        res=user.calc_prob(day,state=False)
        return jsonify(res)

class UserProbState(Resource):
    def get(self,username):
        parser = reqparse.RequestParser()
        parser.add_argument('day', type=str)
        args = parser.parse_args()
        day = args.get('day')
        user=models.User(username)
        res=user.calc_prob(day,state=True)
        return jsonify(res)

class NextState(Resource):
    def get(self,username):
        parser = reqparse.RequestParser()
        parser.add_argument('day', type=str)
        parser.add_argument('hour',type=int)
        args = parser.parse_args()
        day = args.get('day')
        hour= args.get('hour')
        user=models.User(username)
        res=user.next_state(day,hour)
        return jsonify(res)

class CurrentState(Resource):
    def get(self,username):
        user=models.User(username)
        return jsonify(user.get_current_state())

class Timeline(Resource):
    def get(self):
        return app.send_static_file('timeline.html')

api.add_resource(HelloWorld, '/')
api.add_resource(UserData,"/user/<string:username>")
api.add_resource(UserProb,"/user/<string:username>/prob")
api.add_resource(StatePercent,"/user/<string:username>/states")
api.add_resource(UserProbState,"/user/<string:username>/prob/states")
api.add_resource(NextState,"/user/<string:username>/nextstate")
api.add_resource(CurrentState,"/user/<string:username>/CurrentState")
api.add_resource(Timeline,"/timeline")

if __name__=="__main__":
	app.run(host="0.0.0.0",port=4000)
