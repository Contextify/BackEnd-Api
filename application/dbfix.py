from pymongo import MongoClient,errors
import arrow
def fix():
    client = MongoClient('localhost', 27017)
    db=client.contextify
    loc=db.location
    res=list(loc.find({"User":"Sriram","Start":{"$gt":1480309200,"$lt":}}))
    for i,j in zip(res,res[1:]):
        if i["State"]==j["State"]:
            res=loc.find_one(i)
            if res:
                print list(res)
                loc.update({res["_id"]},{"$set":{"End":j["End"]})
                loc.remove(j)

fix()
