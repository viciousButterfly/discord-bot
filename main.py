import nextcord
from nextcord.ext import commands
from nextcord import Embed
import os
from dotenv import load_dotenv
import scrapper 
import github
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
@bot.command()
async def hi(ctx):
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
    embed=Embed(color=0x0080ff, title="Bot Commands")
    embed.add_field(name="Command: hi", value="**Syntax: !hi** \n**_Use:_** Greets you...", inline=False)
    embed.add_field(name="Command: cofsug", value="**Syntax: !cofsug**\n**_Use:_** Get information about CoFSUG.", inline=False)
    embed.add_field(name="Command: socials", value="**Syntax: !socials**\n**_Use:_** Get social media handles of CoFSUG.", inline=False)
    embed.add_field(name="Command: github", value="**Syntax: !github name**\n**_Use:_** Gives top 5 GitHub repos on topic 'name'", inline=False)
    embed.add_field(name="Command: foss", value="**Syntax: !foss**\n**_Use:_** Get latest blog from itsfoss.", inline=False)
    embed.add_field(name="Command: poll", value="**Syntax: !poll choice1 choice2 question**\n**_Use:_** Creates a poll for you :)", inline=False)
    await ctx.send(embed=embed)


#
# @returns cofsug socials
#
@bot.command()
async def socials(ctx):
    await ctx.send("*Checkout our socials :* \n**Instagram** : https://www.instagram.com/cofsug/ \n**LinkedIn** : https://www.linkedin.com/company/coep-s-free-software-users-group/ \n **dev.to (blogs)** : https://dev.to/cofsug \n\n")


#
# @returns scraps itsfoss's recent blog
#
@bot.command(name="foss")
async def article(ctx):
    alt,href = scrapper.itsfoss()
    await ctx.send("{}\n{}".format(alt,href))


#
# @returns information about cofsug
#
@bot.command(name="cofsug")
async def cofsug(ctx):
    await ctx.send("COEP's Free Software Users Group is a community of enthusiasts who promote the use of Free Softwares and are strong supporters of Free and Open Source Ideology! ✨ \n\n ")
    await ctx.send("**Visit our website** : https://foss.coep.org.in/cofsug")


#
# @returns finds top5 repos for the given argument
#
@bot.command(name="github")
async def repositories(ctx,arg):

    repos = github.scrape(arg)
    names = []
    links = []
    for item in repos:
        names.append(item[0])
        links.append(item[1])
    
    names = "\n".join(map(str,names)) 
    links = "\n".join(map(str,links)) 

    embed = nextcord.Embed(title="Github",color=nextcord.Color.green())
    embed.add_field(name="Name", value=names, inline="true")
    embed.add_field(name="Link", value=links, inline="true")
    await ctx.send(embed=embed)


#
# @returns creates a poll
#
@bot.command(name="poll")
async def poll(ctx,choice1,choice2,*,topic):
    IST = pytz.timezone('Asia/Kolkata')
    embed = nextcord.Embed(title=topic, description=f"1️⃣\t{choice1}\n2️⃣\t{choice2}",timestamp=datetime.datetime.now(IST),color=nextcord.Color.green())
    embed.set_footer(text=f"Poll by {ctx.author.name}")
    # below url link temporary for now 
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1035419482476269598/1036862785365221406/Untitled_design1.png?width=581&height=436")
    react = await ctx.send(embed=embed)

    await react.add_reaction("1️⃣")
    await react.add_reaction("2️⃣")

    await ctx.message.delete()


#
# @returns clear messages (only for role with name='Admin')
#
@bot.command()
@commands.has_role('Admin')
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)


#
# @returns a daily scheduled message
#
async def schedule_daily_message():
    now = datetime.datetime.now()
    # then = now + datetime.timedelta(days=1)
    then = now.replace(hour=13,minute=38)
    wait_time = (then-now).total_seconds()
    await asyncio.sleep(wait_time)
    # Channel ID to be changed according to server
    channel = bot.get_channel(1054287735646584905)
    alt,href = scrapper.itsfoss()
    await channel.send("{}\n{}".format(alt,href))


#
# @returns printing bot is ready on terminal
#
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    #await schedule_daily_message()


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
        await ctx.send("*This command is not listed in my dictionary.*")

#
# @Running the bot
#
if __name__ == "__main__": 
    load_dotenv()
    bot.run(os.getenv("DISCORD_TOKEN"))  
