import os
import discord
from keep_alive import keep_alive

import youtube_dl
from discord.ext import commands

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
  print("Logado como {0.user}".format(client))

@client.command()
async def play(ctx, url: str):
  song_there = os.path.isfile("song.mp3")
  try:
    if song_there:
      os.remove("song.mp3")
  except PermissionError:
    await ctx.respond("Espera a musica terminar corno")

  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="General")
  try:
    await voiceChannel.connect()
  except:
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
  }
  try:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
    for file in os.listdir('./'):
      if file.endswith('.mp3'):
        os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
  except Exception:
    await ctx.send("Coloca um link porra")

@client.command()
async def leave(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice is not None:
    await voice.disconnect()
  else:
   await ctx.send("O bot não está conectado à uma sala no momento.")

@client.command()
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
     voice.pause()
  else:
    await ctx.send("O bot não está tocando nada no momento.")

@client.command()
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
  else:
    await ctx.send("O áudio não está pausado.")

@client.command()
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()

keep_alive()
client.run(os.getenv("TOKEN")) 

import discord
import os

class Bot(discord.Client):
  async def on_ready(self):
    print('Logado como: {0}'.format(self.user))

  async def on_message(self,message):
    print('Mensagem de {0.author}: {0.content}'.format(message))

cliente = Bot()
cliente.run(os.getenv("TOKEN"))