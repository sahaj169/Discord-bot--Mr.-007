import discord
from discord.ext import commands , tasks
from discord.utils import get
import random
import os
from os import system
import shutil
import requests
import youtube_dl
import asyncio
from requests_html import AsyncHTMLSession , HTMLSession



client = commands.Bot(command_prefix='?')

status = ['Jamming out to music!','Eating!','Sleeping!']

@tasks.loop(seconds=20)
async def change_status():
	await client.change_presence(activity=discord.Game(random.choice(status)))

@client.event
async def on_ready():
	change_status.start()
	general_channel = client.get_channel(799712402106613821)
	await general_channel.send("Hello,Music Bot is active now!")
	print(f"You have logged in as {client.user}" + " ")




@client.command(name='join',aliases=['j','joi'],help='Bot will join the voice channel')
async def join(ctx):
	if not ctx.message.author.voice:
		await ctx.send('You are not connected to voice channel')
		return
	else:
		channel  = ctx.message.author.voice.channel
		voice = get(client.voice_clients, guild = ctx.guild)
		if voice is not None:
			return await voice.move_to(channel)
		await channel.connect()
		await ctx.send(f"Joined {channel}")

@client.command(aliases = ['paus','pau'],help='Pauses the current music')
async def pause(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)
	if voice and voice.is_playing():
		print("Music paused")
		voice.pause()
		await ctx.send("Music paused")
	else:
		print("Music not playing failed pause")
		await ctx.send("Music not playing failed pause")

@client.command(aliases = ['r','res'],help='resumes the current music')
async def resume(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)
	if voice and voice.is_paused():
		print("Resumed music")
		voice.resume()
		await ctx.send("Resumed music")
	else:
		print("Music is not paused")
		await ctx.send("Music is not paused")

@client.command(aliases=['l','lea'],help='Leave the voice channel')
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild = ctx.guild)
	if voice and voice.is_connected():
		await voice.disconnect()
		print(f"The Bot has left {channel}")
		await ctx.send(f"Left {channel}")
	else:
		# voice = await channel.connect()
		print("Bot was told to leave voice channel, but was not in one")
		await ctx.send("Bot was told to leave voice channel, but was not in one")

@client.command(aliases = ['v','vol'],help='Change the volume of Bot(put volume from 0-100)')
async def volume(ctx, volume:int):
	if ctx.voice_client is None:
		return await ctx.send("Bot not connected to voice channel")
	print(volume/100)
	ctx.voice_client.source.volume = volume/100
	await ctx.send(f"Changed volume to {volume}%")



async def gettingUrl(songName:str):
	asession = AsyncHTMLSession()
	query = songName
	Surl = "https://www.youtube.com/results?search_query="+ str(query)
	r = await asession.get(Surl)
	await r.html.arender(sleep=1, keep_page=True, scrolldown=1, timeout=8.0 * 1000)
	videos = r.html.find('#video-title')
	videoList = []
	for item in videos:
	    video = {
	        'title': item.text,
	        'link': item.absolute_links
	    }
	    videoList.append(video)
	links = ''
	firstItem = videoList[0]['link']
	for i in firstItem:
		links = i
	return links


@client.command(aliases = ['p','pla'],help='Play the music using the URL of the youtube video or full proper name of spotify song')
async def play(ctx,*,songName: str):
	def check_queue():
		Queue_infile = os.path.isdir("./Queue")
		if Queue_infile is True:
			DIR = os.path.abspath(os.path.realpath("Queue"))
			length = len(os.listdir(DIR))
			still_q = length-1
			try:
				first_file = os.listdir(DIR)[0]
			except:
				print("No more queued song(s)\n")
				queues.clear()
				return
			main_location = os.path.dirname(os.path.realpath(__file__))
			song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
			if length !=0:
				print("Song done, playing next queued\n")
				print(f"Songs still in queue: {still_q}")
				song_there = os.path.isfile("Song.mp3")
				if song_there:
					os.remove("Song.mp3")
				shutil.move(song_path,main_location)
				for file in os.listdir("./"):
					if file.endswith(".mp3"):
						os.rename(file,"Song.mp3")
				voice.play(discord.FFmpegPCMAudio("Song.mp3"), after = lambda e: check_queue())
				voice.source = discord.PCMVolumeTransformer(voice.source)
				voice.source.volume = 0.1
			else:
				queues.clear()
				return
		else:
			queues.clear()
			print("No songs were queued before the ending of the last song\n")

	song_there = os.path.isfile("Song.mp3")
	try:
		if song_there:
			os.remove("Song.mp3")
			queues.clear()
			print("Remove old song file")
	except PermissionError:
		print("Trying to delete song file. but it's being played")
		await ctx.send("ERROR: Music Playing")
		return
	Queue_infile = os.path.isdir("./Queue")
	try:
		Queue_folder = "./Queue"
		if Queue_infile is True:
			print("Removed old Queue Folder")
			shutil.rmtree(Queue_folder)
	except:
		print("No old Queue Folder")
	await ctx.send("Getting everything ready now")
	voice = get(client.voice_clients, guild=ctx.guild)


	ydl_opts = {
		'format':'bestaudio/best',
		'quiet':True,
		'outtmpl':"./Song.mp3",
		'postprocessors': [{
			'key':'FFmpegExtractAudio',
			'preferredcodec':'mp3',
			'preferredquality':'320',
		}],
	}
	url = await gettingUrl(songName)
	if url:
		song_search = "".join(url)
	else:
		await ctx.send("Please put a valid url")
	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			print("Downloading audio now\n")
			ydl.download([f"ytsearch1:{song_search}"])
	except:
		print("FALLBACK: youtube_dl does not support this URL, using spotify (This is normal if spotify URL)")
		c_path = os.path.dirname(os.path.realpath(__file__))
		system("spotdl -ff Song -f " +'"' + c_path + '"' + " -s " + song_search)
	voice.play(discord.FFmpegPCMAudio("Song.mp3"), after = lambda e: check_queue())
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07


queues = {}
Listqueue = []
@client.command(aliases = ['q','que'],help='Add song to the Queue')
async def queue(ctx,*,songName:str):
	Listqueue.append(" ".join(songName))
	Queue_infile = os.path.isdir("./Queue")
	if Queue_infile is False:
		os.mkdir("Queue")
	DIR = os.path.abspath(os.path.realpath("Queue"))
	q_num = len(os.listdir(DIR))
	q_num +=1
	add_queue = True
	while add_queue:
		if q_num in queues:
			q_num +=1
		else:
			add_queue = False
			queues[q_num] = q_num
	queue_path = os.path.abspath(os.path.realpath("Queue") + f"\\Song{q_num}.%(ext)s")
	ydl_opts = {
		'format':'bestaudio/best',
		'quiet':True,
		'outtmpl':queue_path,
		'postprocessors': [{
			'key':'FFmpegExtractAudio',
			'preferredcodec':'mp3',
			'preferredquality':'320',
		}],
	}
	url = await gettingUrl(songName)
	if url:
		song_search = " ".join(url)
	else:
		await ctx.send("Please put a valid url")
	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			print("Downloading audio now\n")
			ydl.download([f"ytsearch1:{song_search}"])
	except:
		print("FALLBACK: youtube_dl does not support this URL, using spotify (This is normal if spotify URL")
		q_path = os.path.abspath(os.path.realpath("Queue"))
		system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + song_search)
	await ctx.send("Adding song "+str(q_num) + " to the queue")
	print("Song added to queue\n")


@client.command(aliases = ['s','sto'],help='Stop the song and clear the queue')
async def stop(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)
	queues.clear()
	Queue_infile = os.path.isdir("./Queue")
	if Queue_infile is True:
		shutil.rmtree("./Queue")
	if voice and voice.is_playing():
		print("Music Stopped")
		voice.stop()
		await ctx.send("Music Stopped")
	else:
		print("No music playing to stop")
		await ctx.send("No music playing to stop")


@client.command(aliases = ['n','nex'],help='Plays the Next song from the queue')
async def next(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)
	if voice and voice.is_playing():
		print("Playing next song")
		voice.stop()
		await ctx.send("Next Song")
	else:
		print("No music playing, failed to play nex song")
		await ctx.send("No music playing, failed to play next song")


@client.command(name='listqueue',help='Returns the Queue of songs')
async def view(ctx):
	await ctx.send(f'Your queue is now!')
	j = 1
	for i in Listqueue:
		print(f"{j}. -> {i}")
		await ctx.send(f"{j}. -> {i}")
		j +=1

@client.command(name='remove')
async def remove(ctx, number):
	QueueList = []
	for path, dirs, files in os.walk("./Queue"):
		for f in files:
			QueueList.append(f)
	songdelete = str(QueueList[number+1])
	song_there = os.path.isfile(songdelete)
	try:
		if song_there:
			os.remove(songdelete)
			print(f"{Listqueue[number+1]} is removed from the queue")
			await ctx.send(f"{Listqueue[number+1]} is removed from the queue")
	except PermissionError:
		print("Trying to delete song file. but there is an error")
		return

            #-----------------------------------------------------------------------------------
@client.event
async def on_disconnect():
	general_channel = client.get_channel(799712402106613821)
	await general_channel.send("Music Bot is disconnected0")



TOKEN = "ODAzOTU3OTgzOTk4MjQ2OTEy.YBFWOA.thPH7sI0vCGBASPs4BFGo_Mn0yc"
client.run(TOKEN)