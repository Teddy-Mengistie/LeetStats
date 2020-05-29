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

def problems(user_name):
    my_url = f'http://leetcode.com/{user_name}'
    page = requests.get(my_url)
    soup = BeautifulSoup(page.content, 'lxml')
    #num problems done/1453
    num_probs = soup.get_text().replace("\n", "")
    if("/" in num_probs):
        begin = num_probs.find("Progress")+8
        end = num_probs.find("Solved Question")
        ret = num_probs[begin: end].strip()
        end = ret.find("/")
        return int(ret[0:end])
    else:
        return -1

while(True):
    all = collection.find()
    for x in all:
        b = x["_id"]
        collection.update_one({"_id":b},{"$set":{"week": problems(b) - x["problems"]}})
    time.sleep(15)
