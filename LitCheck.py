import discord
import random
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
import json
#sync method

#Data base connection initation
cluster = MongoClient('MONGODB SERVER ADDRESS')
collection = cluster["Bot"]["Leetcode Users Data"]

client = commands.Bot(command_prefix = "&")
client.remove_command("help")
#-------------------------
#-------events------------
#-------------------------
@client.event
async def on_ready():
    print('Ready!')

@client.event
async def on_command_error(ctx, error):
    messages = ["```diff\n- try again```", "```diff\n- misspelled something?```", "```diff\n- check again```"]
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send(random.choice(messages))
        await help(ctx)

#-------------------------
#-------helper------------
#-------------------------

def problems(user_name):
    my_url = f'http://leet-api2.herokuapp.com/users/{user_name}'
    page = requests.get(my_url) 
    soup = BeautifulSoup(page.content, 'html.parser')
    num_probs = soup.get_text().replace("\n", "")
    
    # 'Application Error'
    if(num_probs.index('{') == -1):
        return -1
        
    problems_solved = json.loads(num_probs)
    return int(problems_solved["total"])
    
#-------------------------
#-------commands----------
#-------------------------
    
@client.command()
async def user(ctx, user_name):
    j = problems(user_name)
    message = discord.Embed(colour = random.randint(0, 0xffffff))
    message.set_author(name = user_name.capitalize().replace("_", "").replace("-", ""))
    message.add_field(name = 'Completed Problems', value = j)
    await ctx.channel.send(embed = message)
    
@client.command()
async def update(ctx):
    all = collection.find()
    count = 0
    for x in all:
        user = x["_id"]
        collection.update_many({"_id":user},{"$set":{"week": problems(user) - x["problems"]}})
        message = f'Updated user {user}'
        print(message)
    await ctx.channel.send("```diff\n+ Done!```")
    
@client.command(name = "reset")
@commands.has_role("leetcode-manager")
async def reset(ctx):
    all = collection.find()
    for x in all:
        b = x["_id"]
        collection.update_many({"_id":b},{"$set":{"problems": x["problems"] + x["week"]}})
        collection.update_many({"_id":b},{"$set":{"week": 0}})
    await ctx.channel.send("```diff\n+ Reset Successfully!```")

@client.command(name = "request")
async def add_request(ctx, userName):
    m = []
    for r in ctx.channel.guild.roles:
        if(r.name == "leetcode-manager"):
            m = r.members
    if(problems(userName) != -1):
        for x in m:
             await x.send(f'```diff\n-{ctx.author.name.capitalize()} would like to add {userName} to the list!```')
    else:
        await ctx.channel.send("```diff\n- User does not exist!```")

@client.command(name = "add")
@commands.has_role("leetcode-manager")
async def add(ctx, user):
        j = problems(user)
        if(j!=-1):
            collection.insert_one({"_id": user,"username": user,"problems": j, "week":0})
            await ctx.channel.send("```diff\n+ Added Successfully!```")
        else:
            await ctx.channel.send("```diff\n- Add unsuccessfull :(```")

@client.command(name = "rm")
@commands.has_role("leetcode-manager")
async def remove(ctx, user):
    collection.delete_one({"_id":user})
    await ctx.channel.send("```diff\n+ Removed Successfully!```")

@client.command(name = "board")
async def leaderboard(ctx):
    mess = discord.Embed(colour = random.randint(0, 0xffffff))
    mess.set_author(name = 'Updating...')
    updating = False
    all = collection.find().sort("week", -1)
    board = "```{:^74}\n{:^30}{:^25}{:^19}\n".format("***LEADERBOARD***","users", "prob's done", "total")
    c = 0;
    for x in all:
        if(x["week"] < 0 or x["problems"] + x["week"] < 0):
            updating = True
        board += "{:>4}){:^25}{}{:^25}{}{:^22}\n".format(c+1, x["_id"], ":", x["week"], ":", x["problems"] + x["week"])
        c+=1
    board+="```"
    if(not updating):
        await ctx.channel.send(board)
    else:
        await ctx.channel.send(embed = mess)

@client.command(name = "clr")
@commands.has_role("leetcode-manager")
async def clr_leet(ctx):
    collection.delete_many({})
    await ctx.channel.send("```diff\n+ Cleared Successfully!```")



@client.command(name = "help", pass_context=True)
async def help(ctx):
    commands_and_description = ["&user <leetcode username> -- Quick info on the amount of leetcode problems done",
                                "&board -- This shows the current leaderboard rated by the amount of problems done in the current week",
                                "&request <leetcode username> -- Requests one of the managers to add this user to the log",
                                "&update -- updates leaderboard to current stats",
                                "&add <leetcode username> -- This adds the requested username to the log",
                                "&rm <leetcode username> -- This removes a user from the log",
                                "&reset -- resets the leaderboard",
                                "&clr -- deletes and clears all the users from the leaderboard"]
    message = "```Java\n"
    for x in commands_and_description:
        await ctx.channel.send(x + "\n")

client.run('BOT CODE HERE')
