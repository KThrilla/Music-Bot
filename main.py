import discord
import youtube_dl
import os
from keep_alive import keep_alive
from discord.ext import commands

client = commands.Bot(command_prefix = "!")

@client.command()
async def play(ctx, url : str):
  song_there = os.path.isfile("song.mp3")
  try:
    if song_there:
      os.remove("song.mp3")
  except PermissionError:
    await ctx.send("Wait for current song to stop playing or use '!stop' command")
    return

  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
  await voiceChannel.connect()
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
  }
  
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  
  for file in os.listdir("./"):
    if file.endswith(".mp3"):
      os.rename(file, "song.mp3")
  
  voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command()
async def leave(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

  if voice.is_connected():
    await voice.disconnect()
  else:
    await ctx.send("dog i'm not even in the vc")

@client.command()
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send("im not even playing music")

@client.command()
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
  else:
    await ctx.send("we're already playing music")

@client.command()
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  
  voice.stop()

keep_alive()
client.run(os.environ['BotToken'])