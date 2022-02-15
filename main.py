from nextcord.ext import commands
from ChessBot.UI.Converter import Converter
import nextcord
import json
import time
import datetime

with open("private/token.json", "r") as f:
    TOKEN = json.load(f)["BOT_TOKEN"]

intents = nextcord.Intents.default()
intents.members = True
intents.presences = True

BOT = commands.Bot(command_prefix= "!", intents= intents)

# GLOBALS
NAME = "Chess Converter"
BOT_DEV = 942854030898647102
IMAGE = "https://raw.githubusercontent.com/Reverend-Toady/Chess-Conversion-Bot/main/local/chess.jpeg"

@BOT.event
async def on_ready():
    print("bot is online")

    channel = BOT.get_channel(BOT_DEV)
    cur_time = time.strftime("%H:%M:%S")
    cur_date = datetime.datetime.today().strftime('%d/%m/%Y')

    embed = nextcord.Embed(
        title = f"{NAME} is back online and ready perform!",
        color = nextcord.Color.green()
    )

    embed.add_field(
            name = "Date Back Online",
            value = cur_date,
            )

    embed.add_field(
            name = "Time Back Online",
            value = cur_time,
    )

    await channel.send(embed= embed)

@BOT.command()
@commands.is_owner()
async def setup_con(ctx):
    view = Converter()
    embed = nextcord.Embed(
        title= "Convert Game",
        description= "Click on the button to convert your chess.com game to a lichess.com game",
        color= nextcord.Color.green()
    )

    embed.add_field(name= "Converts the last played game", value= "You will be DMed the link to the game")

    await ctx.send(embed= embed, view= view)
    await view.wait()

@BOT.command()
@commands.is_owner()
async def setup_ins(ctx):
    embed = nextcord.Embed(
        title= "INSTRUCTIONS",
        color= nextcord.Color.green()
    )

    embed.set_thumbnail(url= IMAGE)
    embed.add_field(
        name= "LINKING PROFILE",
        value= """
        Run `!link <username>` in `#bot-commands` to add your chess.com profile to the bot database,
        **Please Note:** the username has to be case sensitive and matching to the profile username
        """,
        inline= False
    )

    embed.add_field(
        name= "CONVERTING GAME",
        value= "Just click the button in `#convert-game` to convert your last played game",
        inline= False
    )

    await ctx.send(embed= embed)

cogs = ["Linker"]
for cog in cogs:
    BOT.load_extension(f"ChessBot.Cogs.{cog}")


BOT.run(TOKEN)
