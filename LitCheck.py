import discord
import random
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import json
import os
client = commands.Bot(command_prefix = "&")
os.chdir(r'C:\Users\Bertukan A\Desktop\LitCheck')


@client.event
async def on_ready():
    print('I am ready.')

@client.command()
async def user(ctx, user_name):
    if(await problems(ctx = ctx, user_name = user_name) != -1):
        await ctx.channel.send(f'```{user_name} has solved {await problems(ctx = ctx, user_name = user_name)} problems```')
    else:
        messages = ["```try again```", "```incorrect username```", "```you maybe misspelled something```", "```check again```", "```username... is not responding```"]
        await ctx.channel.send(random.choice(messages))

async def problems(ctx, user_name):
    my_url = f'http://leetcode.com/{user_name}'
    page = requests.get(my_url)
    soup = BeautifulSoup(page.content, 'lxml')
    #num problems done/1453
    num_probs = soup.get_text().replace(" ", "")
    if("/" in num_probs):
        begin = num_probs.find("/1453")-4
        end = num_probs.find("/1453")
        return int(num_probs[begin: end].strip())
    else:
        return -1

async def update_data(users, user, pre_probs):
    if user in users:
        del users[user]
    if not user in users:
        users[user] = {}
        users[user]['problems'] = await problems(users, user_name = user)
        if(await problems(users,user_name = user)-pre_probs == users[user]['problems']):
            users[user]['problems done this week'] = 0
        else:
            users[user]['problems done this week'] = await problems(users,user_name = user)-pre_probs

async def get_list(ctx, users):
        max = 0
        maxs = []
        max_user = ""
        max_users = []

        for x in users:
            greater = False
            k = users[x]["problems"]
            for user in users:
                j = users[user]["problems"]
                if(not j in max_users and not k in max_users):
                    if(j )
            if()
            await ctx.channel.send(f'{max_user}:{max}')

@client.command()
async def save(ctx, user_name):
    x = 0
    with open('leetusers.json', 'r') as f:
        users = json.load(f)
    if user_name in users:
        x = users[user_name]['problems']
    await update_data(users, user_name, pre_probs=x)
    with open('leetusers.json', 'w') as f:
        json.dump(users, f, indent = 4, sort_keys = True)

@client.command()
async def leaderboard(ctx):
    with open('leetusers.json', 'r') as f:
        users = json.load(f)
    await get_list(ctx, users)
    with open('leetusers.json', 'w') as f:
        json.dump(users, f, indent = 4, sort_keys = True)

@client.command(pass_context=True)
async def hlp(ctx):
    await ctx.channel.send("```\"&user <leetcode username goes here>\"```")

@client.command()
async def clear(ctx, amount=10):
    if amount < 50:
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.channel.purge(limit = 50)
client.run('NzEyMDM5MzEwMDYwMjkwMTYx.XsLwsg.qIy94BpCf2pfArV1wVYxzYMEGu0')
