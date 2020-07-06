import discord
from discord.ext import commands
import asyncio
from webserver import keep_alive
import os
import random
import datetime
from discord.utils import get
import time


rechenzeichen = ["+", "-", "/", "*","(",")"]
rechnungszeichen = [",", "."]

#==========
#FUNKTIONEN
#==========





"der bot wird ink. prefix definiert und der help command wird entfernt"         "bot ="
bot = commands.Bot(command_prefix=commands.when_mentioned_or("/"))
GUILD = os.environ.get("GUILD")
bot.remove_command("help")


"das event wenn der bot fertig geladen hat und sich angemeldet hat"               "on_ready"
@bot.event
async def on_ready():
  global guild
  await bot.change_presence(activity=discord.Game(name="/help")) #emoji=discord.PartialEmoji(name="U+1F415")
  print("-----------------")
  print(" ")
  print("Bereit als " + bot.user.name)
  print(" ")
  print("-----------------")
  

"""
@bot.event
async def on_message(ctx):
  print(ctx.content)
"""

"eine funktion die nach einer kurzen zeit eine nachricht wieder löscht"           "send_del"
@asyncio.coroutine
def delete(msg, delay):
  yield from asyncio.sleep(delay)
  try:
    yield from discord.Message.delete(msg)
  except:
    return

@asyncio.coroutine
def send_del(channel, content = "", delay = 0, embed = None):
  newMsg = (yield from channel.send(content)) if content != "" else (yield from channel.send(embed=embed))
  if delay!=0:
    bot.loop.create_task(delete(newMsg, delay))
  return newMsg





#======
#EMBEDS
#======







"neu geschriebener help command, der mit embeds geschrieben ist"                   "help"
@bot.command(aliases=["hilfe", "HILFE", ""])
async def help(ctx):
  await ctx.message.delete()                                           

  embed = discord.Embed(colour=discord.Colour.orange(), timestamp=ctx.message.created_at)
  
  embed.set_author(name=f"BayaBot - Befehle")
  embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)

  embed.add_field(name="Mathe :abacus: IN ARBEIT:octagonal_sign:", value="/mathe\nDu kannst minus (-), plus (+), mal (*), geteilt (/) und Klammern benutzen.\n\n\n\n", inline=False)
  #embed.add_field(name="Moderation:hammer:", value="/ban\n/kick\n/delete\n/status\n", inline=False)
  #embed.add_field(name="Fun:joy:", value="/hallo\n/sag\n/arne\n/counter", inline=False)
  embed.add_field(name="Userinfo :bust_in_silhouette:", value="/userinfo\nZeigt Infos über einen User\n\n\n\n", inline=False)
  embed.add_field(name="Member :busts_in_silhouette:", value="/user\nZeigt Anzahl der User auf dem Server\n\n\n\n", inline=False) 
  embed.add_field(name="Würfel :game_die:", value="/dice\nLass Baya eine Zahl würfeln\n\n\n\n", inline=False)
  embed.add_field(name="Münze <:coin:729684347237564458>", value="/coinflip\nEin Coinflip mit Countdown\n\n\n\n", inline=False)
  embed.add_field(name="Schach <:chessknight:723527888862707823>", value="/chess\nSpiele Schach mit uns\n\n\n\n", inline=False)
  

  #embed.add_field(name="", value="", inline=False)

  await ctx.channel.send(embed=embed)


"userinfo command der infos über einen user sendet"                                "userinfo"
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
  await ctx.message.delete()

  member = ctx.author if not member else member
  roles = [role for role in member.roles]

  embed = discord.Embed(colour=discord.Colour.orange(), timestamp=ctx.message.created_at)

  embed.set_author(name=f"User Info - {member}")
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.avatar_url)

  embed.add_field(name="ID:", value=member.id)
  embed.add_field(name="Servernickname:", value=member.display_name)
  embed.add_field(name="Account erstellt:", value=member.created_at.strftime("%a, %#d %B %Y"))
  embed.add_field(name="Server beigetreten:", value=member.joined_at.strftime("%a, %#d %B %Y"))
  embed.add_field(name=f"Alle Rollen ({len(roles)})", value=" ".join([role.mention for role in roles]))
  embed.add_field(name="Hauptrolle", value=member.top_role.mention)
  embed.add_field(name="Botstatus:", value=member.bot)

  await ctx.send(embed=embed)



"user command der die anzahl der member des servers sendet"                       "user"
@bot.command()
async def user(ctx):
  await ctx.message.delete()

  embed = discord.Embed(colour=discord.Colour.orange())
  
  embed.set_author(name=f"Mitglieder dieses Servers: {bot.get_guild(int(GUILD)).member_count}")

  await ctx.send(embed=embed)



"sendet die seite von lichess plus anleitung"                       "chess"
@bot.command()
async def chess(ctx):
  await ctx.message.delete()

  embed = discord.Embed(colour=discord.Colour.orange())
  
  embed.set_author(name=f"Schach")

  embed.add_field(name="Lichess :earth_africa: ", value="--> https://lichess.org/", inline=False)
  embed.add_field(name="Rolle <:chessknight:723527888862707823>", value="in <#714902574947500131> kannst du Zugriff auf \nalle Schach Kanäle bekommen", inline=False)

  await ctx.send(embed=embed)


#Ping Troll Command
@bot.command()
async def ping(ctx):
    
  embed = discord.Embed(colour=discord.Colour.orange())
  embed.set_author(name=f"Pong!")
  await ctx.send(embed=embed)










#========
#COMMANDS
#========










"clear command der eine anzahl von nachrichten löscht"                            "clear"
@bot.command(aliases=["delete", "dl", "cl", "del"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int=10):
  await ctx.channel.purge(limit=amount + 1)



#Baya macht einen coinflip
@bot.command(aliases=["cf","flip"])
async def coinflip(message):
  coin = ["Kopf","Zahl"]
  flip = random.choice(coin)
  
  msg = await message.send("3")
  
  await asyncio.sleep(0.5)

  await msg.edit(content ="2")

  await asyncio.sleep(0.5)

  await msg.edit(content ="1")

  await asyncio.sleep(0.5)

  await msg.edit(content=f"Es wurde **{flip}** geworfen!")



#Baya würfelt eine Zahl
@bot.command(aliases=["dice","wü"])
async def würfel(ctx):
  würfelergebnisse = [
    ':one:',
    ':two:',
    ':three:',
    ':four:',
    ':five:',
    ':six:',
    ]
  ergebnis = random.choice(würfelergebnisse)  
  await ctx.channel.send(f"Ich habe die {ergebnis} gewürfelt.")







def plus(rechnung):
    pos_plus = rechnung.find("+")                    #plos
    if pos_plus!=-1:
        zahl1 = float(mal(rechnung[:pos_plus]))
        zahl2 = float(plus(rechnung[pos_plus+1:]))
        return zahl1 + zahl2
    else:
        return mal(rechnung)

def mal(rechnung):                                    #mol
    pos_mal = rechnung.find("*")    
    if pos_mal!=-1:
        zahl1 = float(geteilt(rechnung[:pos_mal]))
        zahl2 = float(mal(rechnung[pos_mal+1:]))
        return zahl1 * zahl2
    else:
        return geteilt(rechnung)

def geteilt(rechnung):
    pos_geteilt = rechnung.find("/")                #getoilt
    if pos_geteilt!=-1:
        zahl1 = float(rechnung[:pos_geteilt])
        zahl2 = float(geteilt(rechnung[pos_geteilt+1:]))
        return zahl1 / zahl2
    else:
        return rechnung
def klammern(rechnung):                              #klommern
    posKlammer = rechnung.rfind("(")
    PosI = rechnung.find(")", posKlammer) 
    
    if PosI!=-1 and posKlammer!=-1:
      fst = str(rechnung[:posKlammer])
      sst = str(plus(str(rechnung[posKlammer+1:PosI])))
      tst = str(rechnung[PosI+1:])
      return plus(klammern(fst + sst + tst))
    return str(plus(rechnung))

def rechner(h, msg=None):
    global rechnung
    global hraw
    if len(h) > 0:
        zahl1 = 0
        hraw = h
        rechnung = "".join(char for string in hraw for char in string if char.isdigit() or char in rechenzeichen or char in rechnungszeichen)
        rechnung = rechnung.replace(",", ".")
      
        while zahl1 < len(rechnung):
            if rechnung[zahl1] == "(" and rechnung[zahl1-1] not in rechenzeichen:
                rechnung = rechnung[:zahl1] + "*" + rechnung[zahl1:]
                continue
            zahl1 += 1
        zahl1 = 0
        for i in rechnung:
            if i.isdigit():
                break
            else:
                zahl1 += 1
        rechnungvorz = rechnung[:zahl1].replace("*", "")
        rechnungvorz = rechnungvorz.replace("/", "")
        rechnungvorz = rechnungvorz.replace("+", "")
        while "--" in rechnungvorz:
            rechnungvorz = rechnungvorz.replace("--", "-")
        rechnung = str(rechnungvorz) + str(rechnung[zahl1:])
        while "--" in rechnung:
            rechnung = rechnung.replace("--", "+")
            if rechnung[0] == "+":
                rechnung = rechnung[1:]
        while rechnung[-1] in rechenzeichen:
            rechnung = rechnung[:-1]
        rechnung = rechnung.replace("-", "+-")
        try:
            return klammern(rechnung)
        except Exception as e: 
          print(e)
          return "ERROR"
    else:
        embed = discord.Embed(colour=discord.Colour.blue(), timestamp= msg.created_at)
        
        embed.set_author(name=f"Mathe")
        embed.add_field(name="Schreibe eine Aufgabe!", value="Du kannst minus (-), plus (+), mal (*), geteilt (/) und Klammern benutzen.")
        
        return embed

@bot.command(aliases=["maths", "rechner", "calc"])
async def mathe(ctx, string = ""):
  if isinstance(rechner(string, ctx.message), discord.Embed):
    await ctx.send(embed=rechner(string, ctx.message))
  else:
    await ctx.send(rechner(string, ctx.message))



@bot.command()
async def join(ctx):
  where = ctx.content.split(" ")[1]
  channel = get(ctx.guild.channels, name=where)
  voicechannel = await channel.connent()
  voicechannel.join




KEY = os.environ.get("TOKEN")
bot.run(KEY)
