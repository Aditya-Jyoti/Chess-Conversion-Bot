from nextcord.ext import commands
import nextcord
import json
import time
import datetime

intents = nextcord.Intents.default()
intents.members = True
intents.presences = True

BOT = commands.Bot(command_prefix= "!", intents= intents)

# GLOBALS
NAME = "Chess Converter"
BOT_DEV = 942854030898647102


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

cogs = ["Converter"]
for cog in cogs:
    BOT.load_extension(f"cogs.{cog}")

with open("private/token.json", "r") as f:
    TOKEN = json.load(f)["TOKEN"]

BOT.run(TOKEN)
