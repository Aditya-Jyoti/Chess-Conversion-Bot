import requests
import nextcord
from nextcord.ext import commands

CONVERT_CHANNEL = 942849865065566298

class Converter(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.channel = bot.get_channel(CONVERT_CHANNEL)

    @commands.command(aliases= ["Convert", "convert", "Conv", "conv"])
    async def convert_game(self, ctx):
        def check(msg: nextcord.Message):
            return msg.content.lower() in "yes" and msg.channel.id == CONVERT_CHANNEL

        await ctx.send("please send 'yes' below")

        msg = await self.bot.wait_for("message", check= check)
        await ctx.send(f"user sent a message {msg.content}")

def setup(bot):
    bot.add_cog(Converter(bot))
