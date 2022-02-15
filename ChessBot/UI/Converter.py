import nextcord
import sqlite3
import requests
import datetime
import json

with open("private/token.json", "r") as f:
    TOKEN = json.load(f)["LICHESS_TOKEN"]

def send_lichess_request(pgn: str):

    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://lichess.org',
    'Referer': 'https://lichess.org/paste',
    }

    data = {
        "pgn": pgn,
        "pgnFile": "",
        "analyse": "true"
    }

    r = requests.post('https://lichess.org/import', headers=headers, data=data)
    return r.text.split('<meta property="og:url" content=')[1].split(' />')[0][1:-1]


class Converter(nextcord.ui.View):
    def __init__(self, timeout= None):
        super().__init__(timeout= timeout)

    async def handle_click(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        user = str(interaction.user)
        chess_com_name = ""

        con = sqlite3.connect("local/chess-bot.db")
        cur = con.cursor()

        data = """SELECT * FROM USER"""
        cur.execute(data)
        output = cur.fetchall()

        for rows in output:
            if user in rows:
                chess_com_name = rows[1]
                break

        else:
            message = f"""
            {user} your account chess.com account is currently not added to our database\nplease run `!link <username>` in #bot-commands to add your account
            """
            await interaction.response.send_message(message, ephemeral= True)
            return

        cur.close()
        con.close()

        now = datetime.datetime.now()
        day = now.day
        year = now.year
        month = int(f"0{now.month}") if len(str(now.month)) == 1 else now.month

        link = f"https://api.chess.com/pub/player/{chess_com_name}/games/{year}/{month}/pgn"
        r1 = requests.get(link).text.split("\n\n")
        pgn = "\n\n".join([r1[0], r1[1]]).strip()

        url = send_lichess_request(pgn)

        embed = nextcord.Embed(
            title= "your last game played in chess.com was converted with analysis to a lichess.com game",
            description= f"link to game: {url}",
            color= nextcord.Color.green()
        )
        embed.add_field(name= "Date of Game Played", value= f"{day}/{month}/{year}")

        await interaction.response.send_message("You will be DMed the link to the last chess.com game to lichess.com game",
                ephemeral= True)
        await interaction.user.send(embed= embed)

        return

    @nextcord.ui.button(label= "Convert", style= nextcord.ButtonStyle.gray)
    async def convert_game(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)
        return

