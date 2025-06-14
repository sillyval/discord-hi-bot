import discord
import json
from db import increment_guild, get_guild_interactions, get_guild_greeting_channel, set_guild_greeting_channel, get_guild_admin_role, set_guild_admin_role, remove_channel_from_blacklist, add_channel_to_blacklist, is_blacklisted
from utils import isAdmin

with open("config.json", "r") as file:
    config = json.loads(file.read())

token = config.get("token")
global_id = config.get("global-id", "db/main.db")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
	if message.author == client.user: # prevent an infinite spiral of greetings
		return

	text = message.content.lower()

	if is_blacklisted(message.channel.id):
		return

	if text == "hi":
		increment_guild(global_id)

		if message.guild and message.guild.id:
			increment_guild(message.guild.id)

		await message.channel.send("hi")

	if text == "hi.help":
		helpEmbed = discord.Embed(title="hi commands", description="commands to use hi bot", color=0x0033ff)
		helpEmbed.add_field(name="hi.global", value="returns the count for every single `hi` sent in each server this bot is in!", inline=False)
		helpEmbed.add_field(name="hi.guild (guildID, optional)", value="returns the total `hi`s send in the specified/current guild!", inline=False)
		helpEmbed.add_field(name="hi.greeting [role-locked] (channelID optional)", value="if channelID not present, will return the current greeting channel configured. if present, sets the current greeting channel ID to the ID specified!", inline=False)
		helpEmbed.add_field(name="hi.blacklist [role-locked] (channelID)", value="blacklist the channel ID for `hi` interactions", inline=False)
		helpEmbed.add_field(name="hi.whitelist [role-locked] (channelID)", value="whitelist the channel ID for `hi` interactions (make sure hi bot has access!)", inline=False)
		helpEmbed.add_field(name="hi.adminrole [admin-only] (roleID optional)", value="if roleID not present, will return the current hi bot admin role configured. if present, sets the current admin role ID to the ID specified! users with this admin role will be able to access the other commands", inline=False)
		await message.channel.send(embed=helpEmbed)
	
	if text == "hi.global":
		await message.channel.send(f"global `hi`s: {get_guild_interactions(global_id)}")

	if text.startswith("hi.guild"):
		try:
			id = text[len("hi.guild"):]
			id = int(id)

			await message.channel.send(f"`hi`s in that guild: {get_guild_interactions(id)}")
		except:
			id = message.guild.id if message.guild else 0
			if not id or id is None or id == 0:
				await message.channel.send("couldn't detect guild")
			else:
				await message.channel.send(f"`hi`s in this guild: {get_guild_interactions(id)}")

	if text.startswith("hi.greeting"):

		guildID = message.guild.id if message.guild else -1
		if guildID == -1:
			await message.channel.send("guild not detected!")
			return
		
		if not isAdmin(member=message.author, guild=message.guild):
			await message.channel.send("you don't have permission to use this command!")
			return

		try:
			id = text[len("hi.greeting"):]
			id = int(id)

			if id <= 69420:
				id = None

			set_guild_greeting_channel(guildID, id)

			if id == None:
				await message.channel.send(f"cleared greeting channel")
				return
			
			channel = client.get_channel(id)
			if channel is None:
				await message.channel.send(f"updated greeting channel: {id}\n***THIS CHANNEL CANNOT BE SEEN BY HI BOT AND THEREFORE MIGHT NOT WORK PLS FIX 🥺***")
			else:
				await message.channel.send(f"updated greeting channel: {channel.mention}")

		except:
			id = get_guild_greeting_channel(guildID)
			if id is None:
				await message.channel.send(f"this guild doesn't have a greeting channel set up!")
			else:
				channel = client.get_channel(id)
				if channel is None:
					await message.channel.send(f"current greeting channel: {id}\n***THIS CHANNEL CANNOT BE SEEN BY HI BOT AND THEREFORE MIGHT NOT WORK PLS FIX 🥺***")
				else:
					await message.channel.send(f"current greeting channel: {channel.mention}")

	if text.startswith("hi.adminrole"):

		guildID = message.guild.id if message.guild else -1
		if guildID == -1:
			await message.channel.send("guild not detected!")
			return
		
		if not isAdmin(member=message.author, guild=message.guild, allowAdminRole=False):
			await message.channel.send("you don't have permission to use this command!")
			return

		try:
			id = text[len("hi.adminrole"):]
			id = int(id)

			if id <= 69420:
				id = None

			set_guild_admin_role(guildID, id)

			if id == None:
				await message.channel.send(f"cleared admin role")
				return
			
			await message.channel.send(f"updated admin role: {id}")
	
		except:
			id = get_guild_admin_role(guildID)
			if id is None:
				await message.channel.send(f"this guild doesn't have an admin role set up!")
			else:
				await message.channel.send(f"current admin role: {id}")

	if text.startswith("hi.whitelist"):

		guildID = message.guild.id if message.guild else -1
		if guildID == -1:
			await message.channel.send("guild not detected!")
			return
		
		if not isAdmin(member=message.author, guild=message.guild):
			await message.channel.send("you don't have permission to use this command!")
			return

		try:
			id = text[len("hi.whitelist"):]
			id = int(id)

			remove_channel_from_blacklist(id)

			channel = client.get_channel(id)
			if channel is None:
				await message.channel.send(f"whitelisted channel: {id}\n***THIS CHANNEL CANNOT BE SEEN BY HI BOT AND THEREFORE MIGHT NOT WORK PLS FIX 🥺***")
			else:
				await message.channel.send(f"whitelisted channel: {channel.mention}")
		except:
			await message.channel.send(f"pls provide a channel ID to whitelist")

	if text.startswith("hi.blacklist"):

		guildID = message.guild.id if message.guild else -1
		if guildID == -1:
			await message.channel.send("guild not detected!")
			return
		
		if not isAdmin(member=message.author, guild=message.guild):
			await message.channel.send("you don't have permission to use this command!")
			return

		try:
			id = text[len("hi.blacklist"):]
			id = int(id)

			add_channel_to_blacklist(id)

			channel = client.get_channel(id)
			if channel is None:
				await message.channel.send(f"blacklisted channel: {id}")
			else:
				await message.channel.send(f"blacklisted channel: {channel.mention}")
		except:
			await message.channel.send(f"pls provide a channel ID to blacklist")


@client.event
async def on_member_join(member: discord.member):

	guildID = member.guild and member.guild.id
	if not guildID:
		return

	greetingChannelID = get_guild_greeting_channel(guildID)
	if not greetingChannelID:
		return
	
	greetingChannel = client.get_channel(greetingChannelID)
	if not greetingChannel:
		return
	
	if is_blacklisted(greetingChannelID):
		return
	
	await greetingChannel.send(f'hi {member.mention}')


client.run(token)
