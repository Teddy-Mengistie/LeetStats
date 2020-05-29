import discord
import random
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
from threading import Timer
from threading import Thread
import threading
import os
import time
#sync method

#Data base connection initation
cluster = MongoClient(os.environ['MONGO_CLIENT'])
collection = cluster["Bot"]["Leetcode Users Data"]


while(True){
    all = collection.find()
    for x in all:
        b = x["_id"]
        collection.update_one({"_id":b},{"$set":{"week": problems(b) - x["problems"]}})
    time.sleep(60)
}
