import pymongo
from pymongo import MongoClient
import time

cluster = MongoClient(os.environ['MONGO_CLIENT'])
collection = cluster["Bot"]["Leetcode Users Data"]

while(True):
    if(os.environ['INSTANT_RESET']):
        all = collection.find()
        for x in all:
            b = x["_id"]
            collection.update_many({"_id":b},{"$set":{"problems": x["problems"] + x["week"]}})
            collection.update_many({"_id":b},{"$set":{"week": 0}})
        print("***************************Reset Successful***************************")
        time.sleep(os.environ['RESET_DAYS'] * 24 * 60 * 60)# RESET_DAYS is the amt of days to reset in
    else:
        time.sleep(os.environ['RESET_DAYS'] * 24 * 60 * 60)
        all = collection.find()
        for x in all:
            b = x["_id"]
            collection.update_many({"_id":b},{"$set":{"problems": x["problems"] + x["week"]}})
            collection.update_many({"_id":b},{"$set":{"week": 0}})
        print("***************************Reset Successful***************************")
