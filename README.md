# Leetcode Bot
- command prefix = "&amp;"
- requires a Mongo database and a discord bot token and thats all :)
- requires a role named "leetcode-manager" for your server (leetcode-managers can use commands 'add', 'rm', 'reset', and 'clr')
---
#### Commands
- user <leetcode username> -- total leetcode problems done of this user
- board -- leaderboard ranked by problems done after reset
- update -- update leaderboard to the current stats
- add <leetcode username> -- add the username to the leaderboard
- rm <leetcode username> -- remove a user from the leaderboard
- reset -- reset the leaderboard
- clr -- deletes and clears all the users from the leaderboard
