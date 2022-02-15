import nextcord
from nextcord.ext import commands
import requests
import sqlite3

BOT_COMMANDS = 942849865065566298

class Linker(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.channel = bot.get_channel(BOT_COMMANDS)
        self.link = "https://www.chess.com/member/"

    @commands.command(aliases= ["link", "Link"])
    async def link_account(self, ctx, *, username: str):
        link = self.link + username
        r = requests.get(link)

        if r.status_code != 200:
            embed = nextcord.Embed(
                    title= f"Could not find chess.com member with the username: {username}",
                    description= "Please make sure that the username is accurate and case sensitive",
                    color= nextcord.Color.red()
            )
            await ctx.send(embed= embed)
            return

        con = sqlite3.connect("local/chess-bot.db")
        cur = con.cursor()

        data = """SELECT * FROM USER"""
        cur.execute(data)

        output = cur.fetchall()
        for rows in output:
            if username in rows:
                embed = nextcord.Embed(
                    title= f"There is already a chess.com account linked with the username: {rows[1]}",
                    description= f"Account linked by {rows[0]}",
                    color= nextcord.Color.red()
                )
                await ctx.send(embed= embed)
                return

        cur.execute(f"""INSERT INTO USER VALUES ('{ctx.author}', '{username}')""")

        con.commit()
        cur.close()
        con.close()

        embed = nextcord.Embed(
            title= f"Added {username} to the bot database, account successfully linked",
            color= nextcord.Color.green()
        )

        await ctx.send(embed= embed)


def setup(bot):
    bot.add_cog(Linker(bot))
