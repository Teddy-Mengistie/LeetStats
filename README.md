# LeetStats
##### A discord bot for amount of problems solved in leetcode  
#### Requiremenets
- Mongo database and a discord bot token

```py
cluster = MongoClient('MONGODB ADDRESS HERE')
```
```py
client.run('DISCORD BOT TOKEN HERE')
```

- Role in discord named "leetcode-manager" for your server (leetcode-managers can use commands 'add', 'rm', 'reset', and 'clr')

---
#### Commands
##### prefix is "." (can be changed on line: 23)
```py 
command_prefix = "."
```
```
- user (leetcode username) -- total leetcode problems done of this user
- board -- leaderboard ranked by problems done after reset
- update -- update leaderboard to the current stats
- add (leetcode username) -- add the username to the leaderboard
- rm (leetcode username) -- remove a user from the leaderboard
- reset -- reset the leaderboard
- clr -- deletes and clears all the users from the leaderboard
```
