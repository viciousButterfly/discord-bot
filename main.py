import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import scrapper 


intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello! {ctx.author.mention}")


@bot.command()
async def socials(ctx):
    await ctx.send("Checkout our socials : \nInstagram: https://www.instagram.com/cofsug/ \nLinkedIn: https://www.linkedin.com/company/coep-s-free-software-users-group/ \n")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command(name="a")
async def article(ctx):
    alt,href = scrapper.itsfoss()
    await ctx.send("{}\n{}".format(alt,href))

if __name__ == "__main__": 
    load_dotenv()
    bot.run(os.getenv("DISCORD_TOKEN"))  

