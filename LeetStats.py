import discord
import random
from discord.ext import commands
import requests
import json
import pymongo

#Data base connection initation

"""
Database explanation:
    Fields:
        - _id : the name of the user
        - week: the amount of problems done by the user since the last reset of the leaderboard
        - problems: the total amount of problems done by the user
"""
password = 'MONGODB PASSWORD HERE'
cluster = pymongo.MongoClient('MONGODB ADDRESS'.format(password),
                      server_api = pymongo.server_api.ServerApi('1'))
collection = cluster["DATABASE NAME"]["COLLECTION NAME"]

# Discord
# prefix for the bot
command_prefix = "."
client = commands.Bot(command_prefix = command_prefix)
client.remove_command("help")

# Global variables
messages = ["```diff\n- try again```", "```diff\n- misspelled something?```", "```diff\n- Something is not right```"]
#-------------------------
#-------events------------
#-------------------------
@client.event
async def on_ready():
    print('Ready!')

"""
If the discord user enters a wrong command,
we send an error message followed by the list of valid commands.
"""
@client.event
async def on_command_error(ctx, error):
    
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send(random.choice(messages))
        await help(ctx)

#-------------------------
#---------helpers---------
#-------------------------

"""
Connects with {https://leetcode.com/graphql/} by sending a post request 
with the query string that is required. We get back a JSON format data 
of the user's stats. This method returns the all time problems done.
"""
async def problems(user_name):
    # query string to connect to leetcode and get the user problems solved
    # DONT CHANGE, VERY IMPORTANT
    query = {"query":"\n    query userProblemsSolved($username: String!) {\n  allQuestionsCount {\n    difficulty\n    count\n  }\n  matchedUser(username: $username) {\n    problemsSolvedBeatsStats {\n      difficulty\n      percentage\n    }\n    submitStatsGlobal {\n      acSubmissionNum {\n        difficulty\n        count\n      }\n    }\n  }\n}\n    ","variables":{"username":'{}'.format(user_name)}}
    url = "https://leetcode.com/graphql/"
    r = requests.post(url, json = query)
    data = json.loads(r.text)
    data = data["data"]["matchedUser"]
    if (data is None):
        return -1
    else:
        return data["submitStatsGlobal"]["acSubmissionNum"][0]["count"] # returns all the problems solved

#-------------------------
#---------commands--------
#-------------------------

"""
Sends an embed message containing the amount of problems done by this user.
"""
@client.command()
async def user(ctx, user_name):
    j = await problems(user_name)
    color = random.randint(0, 0xffffff)
    message = discord.Embed(colour = color)
    if(j > -1): # user does exist
        message.set_author(name = user_name.capitalize().replace("_", " ").replace("-", " "))
        message.add_field(name = 'Completed Problems', value = j)
    else: # user does not exist
        message.set_author(name = "Invalid User")
    await ctx.channel.send(embed = message)

"""
Loops through the database to update the week field
"""
@client.command()
async def update(ctx):
    all = collection.find()
    for x in all:
        user = x["_id"]
        p = await problems(user)
        if (p >= 0):
            collection.update_many({"_id":user},{"$set":{"week": p - x["problems"]}})
            print(f'Updated {user}\'s stats')
        else: 
            print(f'Problem updating {user}\'s stats')
    await ctx.channel.send("```diff\n+ Done!```")
    
@client.command()
@commands.has_role("leetcode-manager")
async def reset(ctx):
    all = collection.find()
    for x in all:
        user = x["_id"]
        collection.update_many({"_id":user},{"$set":{"problems": await problems(user)}})
        collection.update_many({"_id":user},{"$set":{"week": 0}})
    await ctx.channel.send("```diff\n+ Reset Successfully!```")

"""
Adds a new user to the database, sends error message if user is nonexistent
"""
@client.command()
async def add(ctx, user):
    res = await problems(user)
    if(len(list(collection.find({"_id" : user}))) <= 0 and res >= 0):
        collection.insert_one({"_id": user, "problems": await problems(user), "week":0})
        await ctx.channel.send(f'```diff\n+ Added {user}!```')
    else:
        await ctx.channel.send(f'```diff\n- Could not add {user}!```')

"""
If the user exists in the database, removes them from it. If the user
is already removed it notifies the users by sending an error message.
Required role : leetcode-manager
"""
@client.command(name = "rm")
@commands.has_role("leetcode-manager")
async def remove(ctx, user):
    if(len(list(collection.find({"_id" : user}))) <= 0):
        await ctx.channel.send(f'```diff\n- {user} already removed!```')
        return
    collection.delete_one({"_id":user})
    await ctx.channel.send(f'```diff\n+ Removed {user}!```')

"""
A string-format generated leaderboard will be sent into the chat that the
command was envoked in. It is sorted by the amount of problems that a user
has done since the last reset, and also secondarily sorted by the all time
problems done by the user.
"""
@client.command(name = "board")
async def leaderboard(ctx):
    all = collection.find().sort([('week', -1), ('problems', -1)])
    board = "```{:^78}\n{:^26}{:^26}{:^26}\n".format("LEADERBOARD","users", "done", "total")
    place = 1;
    for x in all:
        board += "{}{:^25}{}{:^25}{}{:^25}\n".format(place, x["_id"], ":", x["week"], ":", x["problems"] + x["week"])
        place += 1
    board+="```"
    await ctx.channel.send(board)

"""
Deletes every user in the database.
Required role : leetcode-manager
"""
@client.command(name = "clr")
@commands.has_role("leetcode-manager")
async def clr_leet(ctx):
    collection.delete_many({})
    await ctx.channel.send("```diff\n+ Cleared Successfully!```")

"""
Sends the list of the commands in the chat that help was called in.
"""
@client.command(name = "help", pass_context=True)
async def help(ctx):
    # the brackets will be replaced by the command prefix in the for loop after the array
    commands_and_description = ['{}user <leetcode username> -- total leetcode problems done of this user',
                                '{}board -- leaderboard ranked by problems done after reset',
                                '{}update -- update leaderboard to the current stats',
                                '{}add <leetcode username> -- add the username to the leaderboard',
                                '{}rm <leetcode username> -- remove a user from the leaderboard',
                                '{}reset -- reset the leaderboard to original',
                                '{}clr -- deletes and clears all the users from the leaderboard']
    message = "```\n"
    for x in commands_and_description:
        message += x.format(command_prefix) + "\n"
    message += "```"
    await ctx.channel.send(message)

client.run("DISCORD BOT TOKEN HERE")
