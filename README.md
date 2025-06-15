# hi bot
its so easy to run just install discord.py and make a config JSON file with like 
- "token" string thats your discord bot token
- "database-file" not needed (db/main.db by default) but is just a path to wherever you want your .db also make sure to MAKE a .db and like populate it with some tables ill show you what to do in a bit
- "global-id" this is just the guild ID that it uses to store the global-ness i didnt wanna put it into its own table bc like why on earth would i do that, ive got this set to -1

  ## making the database
  make sure sqlite3 is installed and run these commands:
  ```
  CREATE TABLE guilds (
    guildID INT PRIMARY KEY,
    interactions INT,
    greetingChannel INT,
    adminRole INT
  );
  CREATE TABLE blacklist (
    channelID INT PRIMARY KEY
  );
  ```
  now your database is all set up hooray

  ## uhh running the bot
  literally just do like ./run.sh as long as you've done the config.json and db file correctly it will run yayayayayayyay

  ## forks/modifications
  i'm happy for people to fork and modify this stupid bot i made in like an hour but the original is `hi#8957` so if you see a hi bot poser who isn't mine make sure to throw tomatoes or something at them

  ## commands and stuff
  can't be bothered to write them again so here's the embed script as of writing this you can literally just read it from there:
  ```
  helpEmbed = discord.Embed(title="hi commands", description="commands to use hi bot", color=0x0033ff)
	helpEmbed.add_field(name="hi.global", value="returns the count for every single `hi` sent in each server this bot is in!", inline=False)
	helpEmbed.add_field(name="hi.guild (guildID, optional)", value="returns the total `hi`s send in the specified/current guild!", inline=False)
	helpEmbed.add_field(name="hi.greeting [role-locked] (channelID optional)", value="if channelID not present, will return the current greeting channel configured. if present, sets the current greeting channel ID to the ID specified!", inline=False)
	helpEmbed.add_field(name="hi.blacklist [role-locked] (channelID)", value="blacklist the channel ID for `hi` interactions", inline=False)
	helpEmbed.add_field(name="hi.whitelist [role-locked] (channelID)", value="whitelist the channel ID for `hi` interactions (make sure hi bot has access!)", inline=False)
	helpEmbed.add_field(name="hi.adminrole [admin-only] (roleID optional)", value="if roleID not present, will return the current hi bot admin role configured. if present, sets the current admin role ID to the ID specified! users with this admin role will be able to access the other commands", inline=False)
	await message.channel.send(embed=helpEmbed)
  ```

  ### developed by val as a test bot that somehow got enough servers to be verified
