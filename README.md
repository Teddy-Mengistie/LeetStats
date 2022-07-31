# LeetStats
#### Discord bot for retrieving leetcode user statistics. The program currently uses less than 3% of all the data provided, which makes this a potential huge project in the future. This bot is currently very functional and can be used to host competitions amongst leetcode users.

### NEW UPDATES
- New leaderboard where users are ranked on how they did on the last weekly contest hosted by Leetcode.com
- New field in database called "contest" which keeps track of the user's rank in the last weekly contest
### FUTURE PROJECTS
- Update contest rank realtime because Leetcode updates are delayed a week from the actual competition
- Upgrade the current UI, it is just plain text. Planning to use embed messages
- Use new discord.py version, there are exciting things like Buttons and tons of UI additions
- Host the bot on one database, just like other discord bots so that it is available for any server to use.

### Running the program
- All you need to get the code running is a MongoDB collection of your own and a discord bot.
```py
password = 'MONGODB PASSWORD HERE'
cluster = pymongo.MongoClient('MONGODB ADDRESS'.format(password), server_api = pymongo.server_api.ServerApi('1'))
```

```py
client.run('DISCORD BOT TOKEN HERE')
```

- Lastly, have a role in discord named "leetcode-manager" for your server (leetcode-managers can use commands 'add', 'rm', 'reset', and 'clr')

---
#### Commands
##### prefix is "." (can be changed on line: 24)
```py 
command_prefix = "."
```
```
- user (leetcode username) -- total leetcode problems done of this user
- board -- leaderboard ranked by problems done after reset
- weekly -- leaderboard based on last leetcode weekly competition
- update -- update leaderboard to the current stats
- add (leetcode username) -- add the username to the leaderboard
- rm (leetcode username) -- remove a user from the leaderboard
- reset -- reset the leaderboard
- clr -- deletes and clears all the users from the leaderboard
```
