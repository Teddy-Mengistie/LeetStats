import discord
import random
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import json
import os

client = commands.Bot(command_prefix = "&")
#-------------------------
#-------events------------
#-------------------------

@client.event
async def on_ready():
    print('I am ready.')

#-------------------------
#-------commands----------
#-------------------------

@client.command()
async def user(ctx, user_name):
    j = problems(ctx,user_name)
    if(j != -1):
        await ctx.channel.send(f'```{user_name} has solved {j} problems```')
    else:
        messages = ["```try again```", "```incorrect username```", "```you maybe misspelled something```", "```check again```", "```username... is not responding```"]
        await ctx.channel.send(random.choice(messages))

def problems(self, user_name):
    my_url = f'http://leetcode.com/{user_name}'
    page = requests.get(my_url)
    soup = BeautifulSoup(page.content, 'lxml')
    #num problems done/1453
    num_probs = soup.get_text().replace("\n", "")
    if("/" in num_probs):
        begin = num_probs.find("/")-4
        end = num_probs.find("/")
        return int(num_probs[begin: end].strip())
    else:
        return -1

@client.command(name = "reset")
@commands.has_role("leetcode-manager")
async def reset(ctx):
    users[user]["problems"] = problems(users, user)

async def get_list(ctx, users):
    names = []
    probs = []
    for i in users:
        names.append(i)
        j = problems(ctx, i)
        probs.append(j-users[i]["problems"])
    stats = {}
    for i in range(0, len(names)):
        stats.update({names[i] : probs[i]})
    stats_sorted = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    print(stats_sorted)
    y = list(stats_sorted)
    try:
        name, prob = zip(*y)
        board = "```"
        for i in range(0, len(y)):
            board += "{}){:>12} {:>12} {:>12}\n".format(i+1, name[i], ":",prob[i])
        board +="```"
    except ValueError:
        await ctx.channel.send("Add users with &add <userName>")
    await ctx.channel.send(board)

@client.command(name = "addReq")
async def add_request(ctx, userName):
    m = []
    for r in ctx.channel.guild.roles:
         if(r.name == "leetcode-manager"):
             m = r.members
    for x in m:
         await x.send(f'```diff\n-{ctx.author.name.capitalize()} would like to add {userName} to the list!```')

@client.command(name = "add")
@commands.has_role("leetcode-manager")
async def add(ctx, user):
        users = {}
        with open('leetusers.json', 'r') as f:
            users = json.load(f)
            f.close()
        j = problems(ctx, user)
        users[user] = {}
        users[user]["problems"] = j
        with open('leetusers.json', 'w') as f:
            json.dump(users, f, indent = 4, sort_keys = True)
        await ctx.channel.send("```diff\n+Added Successfully!```")

@client.command(name = "rm")
@commands.has_role("leetcode-manager")
async def remove(ctx, user):
    with open('leetusers.json', 'r') as f:
        users = json.load(f)
        f.close()
    del users[user]
    with open('leetusers.json', 'w') as f:
        json.dump(users, f, indent = 4, sort_keys = True)
    await ctx.channel.send("```diff\n+Removed Successfully!```")

@client.command(name = "board")
async def leaderboard(ctx):
    with open('leetusers.json', 'r') as f:
        users = json.load(f)
        f.close()
    await get_list(ctx, users)
    with open('leetusers.json', 'w') as f:
        json.dump(users, f, indent = 4, sort_keys = True)

@client.command(name = "clrl")
@commands.has_role("leetcode-manager")
async def clr_leet(ctx):
    users = {}
    with open('leetusers.json', 'w') as f:
        json.dump(users, f, indent = 4, sort_keys = True)
    await ctx.channel.send("```diff\n+Cleared Successfully!```")

@client.command(name = "clrm")
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=10):
    if amount < 50:
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.channel.purge(limit = 50)

@client.command(name = "h",pass_context=True)
async def help(ctx):
    commands_and_description = ["&user <leetcode username> -- Quick info on the amount of leetcode problems done",
                                "&board -- This shows the current leaderboard rated by the amount of problems done in the current week",
                                "&addReq <leetcode username> -- Requests one of the managers to add this user to the log",
                                "&clr *not required*<specific amount of messages> -- Deleted the amount of messages specified, max = 50, default = 10",
                                "&add <leetcode username> -- This adds the requested username to the log",
                                "&remove <leetcode username> -- This removes a user from the log",
                                "&reset -- resets the leaderboard and the logged data"]
    isManager = False
    i = ctx.author.roles
    k = 3
    for j in i:
        if("leetcode-manager" == j.name):
            isManager = True
            k = 7
    help_message = "```\n"
    for x in range(0, k):
        help_message += commands_and_description[x]
        help_message += "\n\n"
    help_message += "```"
    await ctx.channel.send(help_message)


client.run(os.environ['TOKEN'])
