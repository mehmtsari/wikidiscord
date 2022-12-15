import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import config
from discord.ext import commands
import random
from wiki_fonk import main_wiki_func,search_connect,information_voice
from time import sleep
import os

import asyncio


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.bot.Bot(command_prefix=config.PREFİX,intents= intents,help_command=None)

@bot.event
async def on_ready():
    print("-----")
    print("Bot İs Online")
    print("-----")
    
@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    
    if message.author == bot.user:
        return
    
    if user_message.startswith("!"):
        print(f'Komut İstemi! = {username}: {user_message}  ({channel}) ')
    else:
        print(f'{username}: {user_message}  ({channel}) ')
    
    if user_message.lower() == "!clear_all":
        await message.channel.purge()
        
    if message.channel.name == 'komut-kanalı':
        await bot.process_commands(message)
        
@bot.command()
async def clear_all(ctx):
    await ctx.channel.purge()



@bot.command()
async def help(ctx):
    await ctx.send("     Kılavuz Ve Komutlar\n "+
                   "!help                     $Kılavuz ve Komutlar\n"+
                   "!wiki dökümantasyonadı    $Dökümantasyonu indirilebilir dosya olarak önünüze döker.\n")
    
    
@bot.command()
async def wiki(ctx, *args):
    
    await ctx.send(f"System : Araştırılyor>{args[0]}")
    if search_connect(args[0]) == True:
        sleep(1)
        await ctx.send(f"System: {args[0]} Adlı Dökümantasyon Bulundu. Oluşturuluyor")
        filex = main_wiki_func(args[0]).split("#")
        k = 0
        for i in filex:
            if k == 0:
                await ctx.send("Ses Dosyası:",file=discord.File(i))
                os.remove(i)
                k += 1
            elif k == 1:
                await ctx.send("Slayt Dosyası:",file=discord.File(i))
                os.remove(i)
                k += 1
            elif k == 2:
                await ctx.send("Word Dosyası:",file=discord.File(i))
                os.remove(i)
                k += 1
        await ctx.send(f"{args[0]} Hakkında Dökümantasyon.")
    else:
        await ctx.send(f"System: {args[0]} Adlı Bir Dökümantasyon Bulunamadı. ")
        return



@bot.command()
async def wikimulti(ctx, *args):
    
    for i in args:
        i.upper()
    
        await ctx.send(f"System : Araştırılyor>{i}")
        if search_connect(i) == True:
            sleep(1)
            await ctx.send(f"System: {i} Adlı Dökümantasyon Bulundu. Oluşturuluyor")
            filex = main_wiki_func(i).split("#")
            k = 0
            for i in filex:
                if k == 0:
                    await ctx.send("Ses Dosyası:",file=discord.File(i))
                    os.remove(i)
                    k += 1
                elif k == 1:
                    await ctx.send("Slayt Dosyası:",file=discord.File(i))
                    os.remove(i)
                    k += 1
                elif k == 2:
                    await ctx.send("Word Dosyası:",file=discord.File(i))
                    os.remove(i)
                    k += 1
            await ctx.send(f"{i} Hakkında Dökümantasyon.")
            await ctx.send(f"----------Wikipedia--Asistan----------")
        else:
            await ctx.send(f"System: {i} Adlı Bir Dökümantasyon Bulunamadı. ")
            return



@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.channel.send("You are not connected to a voice channel.")
        return
    #Connect to voice channel
    try:
        await ctx.author.voice.channel.connect()
    except:
        await ctx.guild.voice_client.move_to(ctx.author.voice.channel)

    await ctx.channel.send("Connected.")

@bot.command()
async def leave(ctx):
    if ctx.guild.voice_client is None:

        await ctx.channel.send("Not connected.")
        return

        #Disconnect
        
    await ctx.guild.voice_client.disconnect()

    await ctx.channel.send("I disconnected.")
    
@bot.command()
async def play(ctx):
    if ctx.guild.voice_client is None:
        await ctx.channel.send("Not connected.")
        return
    ctx.guild.voice_client.play(discord.FFmpegPCMAudio("voice-1695.mp3"))



bot.run(config.TOKEN)