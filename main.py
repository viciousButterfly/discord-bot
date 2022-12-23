import nextcord
from nextcord.ext import commands
from nextcord import Embed
import os
from dotenv import load_dotenv
import scrapper 
import utils
import datetime
import pytz
import asyncio
import random


intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")


#
# @returns greeting message
#
@bot.command(name="hi")
async def greeting(ctx):
    greetings = [
        "I hope you're doing well.",
        "I hope you're having a great week.",
        "I hope you're having a wonderful day.",
        "Thanks for getting in touch.",
        "Happy {}.".format(utils.findDay())
    ]
    await ctx.send(f"Hello! {ctx.author.mention}, {random.choice(greetings)}")


#
# @returns help messages for bot commands
#
@bot.command(name="help")
async def Help(ctx):
    embed=Embed(title="Bot Commands", color=0x0080ff)

    embed.add_field(name="Command: hi", value="**Syntax: !hi** \n**_Use:_** Greets you...", inline=False)
    embed.add_field(name="Command: cofsug", value="**Syntax: !cofsug**\n**_Use:_** Get information about CoFSUG.", inline=False)
    embed.add_field(name="Command: socials", value="**Syntax: !socials**\n**_Use:_** Get social media handles of CoFSUG.", inline=False)
    embed.add_field(name="Command: github", value="**Syntax: !github <query>**\n**_Use:_** Get top 5 GitHub repos on given <query>", inline=False)
    embed.add_field(name="Command: foss", value="**Syntax: !foss**\n**_Use:_** Get latest blog from itsfoss.", inline=False)
    embed.add_field(name="Command: poll", value="**Syntax: !poll \<Question>\" c1 c2 ...**\n**_Use:_** Creates a poll for you :)", inline=False)
    embed.add_field(name="Command: profile", value="**Syntax: !profile**\n**_Use:_** Displays your information", inline=False)
    embed.add_field(name="Command: server", value="**Syntax: !server**\n**_Use:_** Displays server information", inline=False)
    embed.add_field(name="Command: ping", value="**Syntax: !ping**\n**_Use:_** Displays latency", inline=False)
    embed.add_field(name="Command: yt", value="**Syntax: !yt <query>**\n**_Use:_** Gets Youtube video according to query", inline=False)
    embed.add_field(name="Command: dict", value="**Syntax: !dict <word>**\n**_Use:_** Gets dictionary meaning of word", inline=False)

    await ctx.send(embed=embed)


#
# @returns cofsug socials
#
@bot.command(name="socials")
async def Socials(ctx):
    await ctx.send("*Checkout our socials :* \n**Instagram** : https://www.instagram.com/cofsug/ \n**LinkedIn** : https://www.linkedin.com/company/coep-s-free-software-users-group/ \n**dev.to** : https://dev.to/cofsug \n\n")


#
# @returns scraps itsfoss's recent blog
#
@bot.command(name="foss")
async def Article(ctx):
    alt,href = scrapper.itsfoss()
    await ctx.send("{}\n{}".format(alt,href))


#
# @returns information about cofsug
#
@bot.command(name="cofsug")
async def About(ctx):
    await ctx.send("**COEP's Free Software Users Group** is a community of enthusiasts who promote the use of Free Softwares and are strong supporters of Free and Open Source Ideology! ✨ \n**Visit our website** : https://foss.coep.org.in/cofsug\n")


#
# @returns finds top5 repos for the given argument
#
@bot.command(name="github")
async def Repositories(ctx,arg):

    repos = scrapper.github(arg)
    names = []
    links = []
    for item in repos:
        names.append(item[0])
        links.append(item[1])
    
    names = "\n".join(map(str,names)) 
    links = "\n".join(map(str,links)) 

    embed = nextcord.Embed(title="Github",
                        color=nextcord.Color.green())

    embed.add_field(name="Name", value=names, inline="true")
    embed.add_field(name="Link", value=links, inline="true")
    await ctx.send(embed=embed)


#
# @ returns top youtube video for the given query
#
@bot.command(name="yt")
async def Youtube(ctx,*arg):
    query = " ".join(arg)
    if query == "":
        return await ctx.send("*Command is missing an argument!* ")

    await ctx.reply(scrapper.youtube(query))


#
# @returns dictionary meaning of a word
#
@bot.command(name="dict")
async def Dictionary(ctx,arg):
    word,meaning = scrapper.dictionary(arg)

    if word == False:
        return await ctx.reply("**Sorry pal, we couldn't find definitions for the word you were looking for.**")
    
    embed = nextcord.Embed(title=word, 
                        description=meaning,
                        color=nextcord.Color.purple())
    await ctx.reply(embed=embed)


#
# @returns creates a poll 
#
@bot.command(name="poll")
async def Poll(ctx,question,*choices):
    IST = pytz.timezone('Asia/Kolkata')
    
    if len(choices) > 10:
        return await ctx.send("**Too many options in the given poll, Max options count restricted to 10!**")

    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    description = ""
    for i in range(len(choices)):
        description+=f"{reactions[i]} {choices[i]}\n"

    embed = nextcord.Embed(title=question, 
                        description=description,
                        timestamp=datetime.datetime.now(IST),
                        color=nextcord.Color.green())

    embed.set_footer(text=f"Poll by {ctx.author.name}")
    embed.set_thumbnail(url=ctx.message.author.display_avatar)
    react = await ctx.send(embed=embed)

    for i in range(len(choices)) :
        await react.add_reaction(reactions[i])

    await ctx.message.delete()


#
# @returns latency in miliseconds
#
@bot.command(name="ping")
async def Ping(ctx):
    embed = nextcord.Embed(
          title="Ping",
          description=f"Ping is `{round(bot.latency * 100, 2)}` ms",
          color=ctx.author.color)

    await ctx.send(embed=embed)


#
# @returns profile information
#
@bot.command(name="profile")
async def Profile(ctx):
    user = ctx.message.author
    embed = Embed(title=user,
                color=nextcord.Color.green())

    userData = {
        "ID" : user.id,
        "Nick": user.nick,
        "Top role" : user.top_role,
        "Created at" : user.created_at.strftime("%b %d, %Y"),
        "Joined at" : user.joined_at.strftime("%b %d, %Y"),
        "Server" : user.guild
    }

    for [name,value] in userData.items():
        embed.add_field(name=name, value=value,inline=True)
    
    embed.set_thumbnail(url=user.display_avatar) 
    
    await ctx.send(embed=embed)


#
# @returns server information
#
@bot.command(name="server")
async def Server(ctx):
    guild = ctx.message.author.guild
    embed = Embed(title=guild.name,
            color=nextcord.Color.green())

    serverData = {
        "Owner" : "CoFSUG",
        "Channels" : len(guild.channels),
        "Members" : guild.member_count,
        "Description" : guild.description
    }

    for [name,value] in serverData.items():
        embed.add_field(name=name, value=value,inline=False) 

    embed.set_footer(text=f"id: {guild.id}")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1035419482476269598/1036862785365221406/Untitled_design1.png?width=581&height=436") 

    await ctx.send(embed=embed)


#
# @returns clear messages (only for role with name='Admin')
#
@bot.command(name="clear")
@commands.has_role('Admin')
async def Clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)


#
# @returns a daily scheduled message
#
async def schedule_daily_message():
    now = datetime.datetime.now()
    then = now + datetime.timedelta(days=1)
    then = then.replace(hour=12,minute=00)
    wait_time = (then-now).total_seconds()

    await asyncio.sleep(wait_time)

    channel = bot.get_channel(os.getenv("CHANNEL_ID"))
    alt,href = scrapper.itsfoss()
    await channel.send("{}\n{}".format(alt,href))


#
# @returns printing bot is ready on terminal
#
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await schedule_daily_message()


#
# @handles Handling errors
#
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send("*Private messages.* ")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("*Command is missing an argument!* ")
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("*This command is currenlty disabled. Please try again later.* ")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("*You do not have the permissions to do this.* ")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("*This command is not listed in my dictionary.*\n**Try !help for more info.**")

#
# @Running the bot
#
if __name__ == "__main__": 
    load_dotenv()
    bot.run(os.getenv("DISCORD_TOKEN"))  
