import discord
from discord.ext import commands , tasks
from discord.utils import get
import random
import json
import os
from os import system
import shutil
import requests
import youtube_dl
import asyncio
from requests_html import AsyncHTMLSession , HTMLSession



client = commands.Bot(command_prefix='$')



status = ['Jamming out to music!','Eating!','Sleeping!']

@tasks.loop(seconds=20)
async def change_status():
	await client.change_presence(activity=discord.Game(random.choice(status)))

YOURGUILDSID = 799703559615545415
YOURID =   702105495841800214
YOURFILENAME = "users.json"

# m = {}

@client.event
async def on_ready():
	change_status.start()
	general_channel = client.get_channel(799712402106613821)
	await general_channel.send("Hello,Bot is active now!")
	print(f"You have logged in as {client.user}" + " ")
	# for memberss in client.get_all_members():
	# 	print(memberss)
	# global m
	# with open(YOURFILENAME, "r") as j:
	# 	m = json.load(j)
	# 	j.close()
	# if len(m) == 0:
	# 	m = {}
	# 	for member in client.get_guild(YOURGUILDSID).members:
	# 		m[str(member.id)] = {"xp" : 0, "messageCountdown" : 0}
	# 	with open(YOURFILENAME, "w") as j:
	# 		j.write( json.dumps(m))
	# while True:
	# 	try:
	# 		for member in client.get_guild(YOURGUILDSID).members:
	# 			m[str(member.id)]["messageCountdown"] = -1
	# 	except:
	# 		pass
	# 	await asyncio.sleep(1)



# @client.event
# async def on_member_join(member):

# 	# m[str(member.id)] = {"xp" : 0, "messageCountdown" : 0}

# 	# channel = discord.utils.get(member.guild.channels, name='general')
# 	channel = discord.utils.get(guild.text_channels, name="general")
# 	# channel = client.get_channel(799712402106613821)
# 	print(channel)
# 	print(f'Welcome {member.mention}!  Everyone say Hi!. Use `$help` command for details!')

# 	await channel.send(f'Welcome {member.mention}!  Everyone say Hi!. Use `$help` command for details!')

@client.event
async def on_member_join(member):

	channel = member.guild.get_channel(799703560072855583)
	await channel.send("welcome {} to {} ".format(str(member.mention),str(member.guild)))

@client.event
async def on_message(message):
	# global m
	# if message.content == "!stop" and message.author.id == YOURID:
	# 	with open(YOURFILENAME, "w") as j:
	# 		j.write( json.dumps(m) )
	# 		j.close()
	# 	await client.close()
	# elif message.content == "!xp":
	# 	await message.channel.send( str(m[str(message.author.id)]["xp"]) )
	# elif message.author != client.user:
	# 	if m[str(message.author.id)]["messageCountdown"] <= 0:
	# 		m[str(message.author.id)]["xp"] += 10
	# 		m[str(message.author.id)]["messageCountdown"] = 10

#--------------------------------------------------------------------------------------------------------------------
	 #-----------------------------
	if message.author == client.user:
		return
	if db["responding"]:
		options = starter_encouragements
		if "encouragements" in db.keys():
			options = options + db["encouragements"]
		if any(word in message.content for word in sad_words):
			general_channel = client.get_channel(799712402106613821)
			await general_channel.send(random.choice(options))
	#------------------------------------------------------------------
	await client.process_commands(message)
#------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(help='return the latency')
async def ping(ctx):
	await ctx.send(f'**Ping!** Latency: {round(client.latency * 1000)}ms')


#add more interesting greetings
@client.command(name='hello',aliases=['hy','hi','hey','hello bot'],help='return a random welcome message')
async def hello(ctx):
	responses = ['**grumble** Why did you wake me up?','Hello! My name is Mrs. Bot 007','Welcome!','How may I help you',]
	await ctx.send(random.choice(responses))

#can add random bye messages into this 
@client.command(name="bye", help='says bye')
async def bye(ctx):
	await ctx.send("Bye! Thank You")

#die can also use to make bot leave the server
@client.command(name='die', help='returns a random last words')
async def die(ctx):
	responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
	await ctx.send(random.choice(responses))

#use embeds for credits 
@client.command(name="credits", help='returns the credits')
async def credits(ctx):
	await ctx.send('Made by Sahaj Ghaatiya')
	await ctx.send('Thanks for using the Bot')


#Add more functionaly in this, such as 
@client.command(name="dm",help='sends a DM to You')
async def dm(ctx):
	await ctx.author.send('**This is a DM from Mrs Bot 007**, How May I help you sir')

def is_me(m):
	return m.author == client.user

@client.command(help='clear the specific amount of messages from the channel')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit=amount+1)
	await ctx.send(f"{amount} number of messages are deleted from the channel")

@client.command(name='kick',help='Kick the mentioned member from the server')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
	await member.kick()
	await ctx.send('User ' +member.display_name+' has been kicked.')

@client.command(name='ban',help='Bans the mentioned member from the server')
@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send('User ' +member.display_name+' has been banned.')


@client.command(name='unban',help='unban the mentioned member from the server')
@commands.has_permissions(kick_members=True)
async def unban(ctx,*,member):
	banned_users = await ctx.guild.bans()
	member_name,member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		if (user.name,user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f"unbanned {user.mention}")
			return

@client.command(name='version',help='return the version information of the Bot')
async def version(ctx):    
	myEmbed = discord.Embed(title = "Current Version", description = "The Bot is in Version 1.0", color = 0x00ff00)
	myEmbed.add_field(name="Version Code:",value="v1.0.0",inline=False)
	myEmbed.add_field(name="Date Released:", value="September 16th, 2021",inline=False)
	myEmbed.set_footer(text="This is a sample Footer")
	myEmbed.set_author(name="Sahaj Ghaatiya")
	await ctx.message.channel.send(embed=myEmbed)

#------------------------------------------------------------------------------------------------------------------------------------------    
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.command(name="inspire",help='send a inspiring quote')
async def inspire(ctx):
	quote = get_quote()
	await ctx.send(quote)

#-----------------------This part is for sad word response and encouragements section------------

db={}

sad_words = ["sad","depressed","unhappy","angry","miserable","depressing"]
starter_encouragements = ["Cheer up!","Hang in there.","You are a great person / bot !!"]

if "responding" not in db.keys():
  db["responding"] = True

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
  	encouragements = db["encouragements"]
  	encouragements.append(encouraging_message)
  	db["encouragements"] = encouragements
  else:
  	db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
  	del encouragements[index]
  	db["encouragements"] = encouragements

@client.command(name="add",help='add the given encouraging message to the encouragements list')
async def add(ctx,*,message):
	encouraging_message = message
	update_encouragements(encouraging_message)
	await ctx.send("New encourageing message added.")

@client.command(name="delete",help='delete the choosen encouragement from the list of encouragements')
async def delete(ctx,index:int):
	encouragements = []
	if "encouragements" in db.keys():
		delete_encouragement(index-1)
		encouragements = db["encouragements"]
	await ctx.send(encouragements)

@client.command(name="list",aliases=['list encouragements'],help='return the List of encouragements')
async def list(ctx):
	encouragements = []
	if "encouragements" in db.keys():
		encouragements = db["encouragements"]
	await ctx.send(encouragements)

@client.command(name="responding",help='help us to control the functionality of responding to sad words in the chats')
async def responding(ctx,value):
	if value.lower() == "true":
		db["responding"] = True
		await ctx.send("Responding to sad message is on")
	if value.lower() == "false":
		db["responding"] = False
		await ctx.send("Responding to sad message is off")



#-------------------------------------------------------------------------------------------
reaction_title = ""
reactions = {}
reaction_message_id = ""

@client.command(name="reaction_create_post",help='create a reaction post')
async def reaction_create_post(ctx):
	embed = discord.Embed(title="Create Reaction Post",color = 0x8cc542)
	embed.set_author(name="Mrs. Bot 007")
	embed.add_field(name="Set Title", value="$reaction_set_title \"New Title\"",inline=False)
	embed.add_field(name="Add Role", value="$reaction_add_role @Role EMOJI_HERE",inline=False)
	embed.add_field(name="Remove Role", value="$reaction_remove_role @Role",inline=False)
	embed.add_field(name="Send Creation Post", value="$reaction_send_post",inline=False)

	await ctx.send(embed=embed)
	await ctx.message.delete()

@client.command(name="reaction_set_title",help='')
async def reaction_set_title(ctx, new_title):

	global reaction_title
	reaction_title = new_title
	await ctx.send("Title for the message is now `" + reaction_title + "`!")
	await ctx.message.delete()

@client.command(name="reaction_add_role",help='')
async def reation_add_role(ctx,role: discord.Role,reaction):

	if role != None:
		reactions[role.name] = reaction
		await ctx.send("Role `" + role.name + "` has been added with the emoji "+ reaction)
		await ctx.message.delete()
	else:
		await ctx.send("Please try again!")

	print(reactions)

@client.command(name="reaction_remove_role")
async def reaction_remove_role(ctx,role:discord.Role):
	if role.name in reactions:
		del reactions[role.name]
		await ctx.send("Role `" + role.name + "` has been deleted!")
		await ctx.message.delete()
	else:
		await ctx.send("That role has not been added")
	print(reactions)

@client.command(name="reaction_send_post")
async def reaction_send_post(ctx):
	description = "React to add the roles!\n"

	for role in reactions:
		description += "`" + role + "`" + reactions[role]+"\n"

	embed = discord.Embed(title=reaction_title,description = description,color=0x8cc542)
	embed.set_author(name="Mrs. Bot 007")

	message = await ctx.send(embed=embed)

	global reaction_message_id
	reaction_message_id = str(message.id)

	for role in reactions:
		await message.add_reaction(reactions[role])
	await ctx.message.delete()

@client.event
async def on_reaction_add(reaction,user):
	if not user.bot:
		message = reaction.message

		if str(message.id) == reaction_message_id:
			#Add role to our users
			role_to_give = ""
			for role in reactions:
				if reactions[role] == reaction.emoji:
					role_to_give = role
				role_for_reaction = discord.utils.get(user.guild.roles,name = role_to_give)
				await user.add_roles(role_for_reaction)



#---------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------
@client.command()
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('please pass in all required arguments.')




#----------------------------------------------------------Music Bot---------------------------------------------------

client.run("bot token here")



		













# async def update_data(users,user):
# 	if user.id not in users:
# 		users[user.id] = {}
# 		users[user.id]['experience'] = 0
# 		users[user.id]['level'] = 1

# async def add_experience(users,user):
# 	users[user.id]['experience'] += 5

# async def level_up(users,user,channel):
# 	experience = users[user.id]['experience']
# 	lvl_start = users[user.id]['level']
# 	lvl_end = int(experience ** (1/4))
# 	if lvl_start < lvl_end:
# 		await client.send_message(channel,f"{user.mention} has leveled up to level {lvl_end}")
# 		users[user.id]['level'] = lvl_end


	# with open('users.json','r') as f:
	# 	users = json.load(f)

	# await update_data(users,member)

	# with open('users.json','w') as f:
	# 	json.dump(users,f)

	
	# with open('users.json','r',encoding='utf8') as f:
	#     user = json.load(f)
	# try:
	#     with open('users.json','w',encoding='utf8') as f:
	#		  
	#         user[str(message.author.id)]['exp'] +=1
	#         lvl_start = user[str(message.author.id)]['level']
	#         lvl_end = user[str(message.author.id)]['exp'] ** (1/10)
	#         if lvl_start < lvl_end:
	#             user[str(message.author.id)]['level'] = user[str(message.author.id)]['level'] +1
	#             lvl = user[str(message.author.id)]['level']
	#             await message.channel.send(f"{message.author.mention} has leveled up to {lvl}")
	#             json.dump(user, f,sort_keys=True,indent=4,ensure_ascii=False)
	#             return
	#         json.dump(user, f,sort_keys=True,indent=4,ensure_ascii=False)
	# except:
	#     with open('users.json','w'.encoding='utf8') as f:
	#         user = {}
	#         user[str(message.author.id)]={}
	#         user[str(message.author.id)]['level'] = 0
	#         user[str(message.author.id)]['exp'] = 0
	#         json.dump(user, f,sort_keys=True,indent=4,ensure_ascii=False)


	# with open('users.json','r') as f:
	# 	users = json.load(f)

	# await update_data(users,message.author)
	# await add_experience(users,message.author)
	# await level_up(users,message.author,message.channel)


	# with open('users.json','w') as f:
	# 	json.dump(users,f)


















# @client.command()
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send('please use a valid command')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# youtube_dl.utils.bug_reports_message = lambda: ''

# ytdl_format_options = {
#     'format': 'bestaudio/best',
#     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
# }

# ffmpeg_options = {
#     'options': '-vn'
# }

# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get('title')
#         self.url = data.get('url')

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]

#         filename = data['url'] if stream else ytdl.prepare_filename(data)
#         return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# queue = []

# @client.command(name='queue')
# async def queue_(ctx, url):
#     global queue
#     queue.append(url)
#     await ctx.send(f'`{url}` added to queue!')


# @client.command(name='play', help='plays a song')
# async def play(ctx):
#   global queue
#   server = ctx.message.guild
#   voice_channel = server.voice_client
#   async with ctx.typing():
#       player = await YTDLSource.from_url(queue[0],loop=client.loop)
#       voice_channel.play(player,after=lambda e: print('Player error: %s' %e) if e else None)
#   await ctx.send(f'**Now Playing:** {player.title}')
#   del(queue[0])


# @client.command(name="stop", help='stops the song')
# async def stop(ctx):
#     server = ctx.message.guild
#     voice_channel = server.voice_client
#     voice_channel.stop()
#----------------------------------------------------------------------------------------------------------------------------------------
