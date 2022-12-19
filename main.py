import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import scrapper 
import github
import datetime
import pytz


intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# greeting command
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello! {ctx.author.mention}")

# socials command to display socials
@bot.command()
async def socials(ctx):
    await ctx.send("*Checkout our socials :* \n**Instagram** : https://www.instagram.com/cofsug/ \n**LinkedIn** : https://www.linkedin.com/company/coep-s-free-software-users-group/ \n\n")

# foss command to scrap itsfoss's recent blog
@bot.command(name="foss")
async def article(ctx):
    alt,href = scrapper.itsfoss()
    await ctx.send("{}\n{}".format(alt,href))

# github command to find top5 repos for the given argument
@bot.command(name="github")
async def repositories(ctx,arg):
    repos = github.scrape(arg)
    message = "*Here are Top {} repos:*".format(len(repos))

    for item in repos:
        message+="\n⦁ Name : {}\n\t`Link` : {}".format(item[0],item[1])

    await ctx.send(message)

# poll command to create a poll
@bot.command(name="poll")
async def poll(ctx,choice1,choice2,*,topic):
    IST = pytz.timezone('Asia/Kolkata')
    embed = nextcord.Embed(title=topic, description=f"1️⃣\t{choice1}\n2️⃣\t{choice2}",timestamp=datetime.datetime.now(IST))
    embed.set_footer(text=f"Poll by {ctx.author.name}")
    react = await ctx.send(embed=embed)

    await react.add_reaction("1️⃣")
    await react.add_reaction("2️⃣")

    await ctx.message.delete()

# clear command to clear messages (only for role with name='Admin')
@bot.command()
@commands.has_role('Admin')
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)

# printing bot is ready on terminal
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Handling errors
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

# Running the bot
if __name__ == "__main__": 
    load_dotenv()
    bot.run(os.getenv("DISCORD_TOKEN"))  
