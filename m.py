from pymongo import MongoClient,errors
import arrow

client = MongoClient('localhost', 27017)
db=client.contextify
