import requests
import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
token = os.getenv('DISCORD_TOKEN')

# store matches that have already been posted to the discord channel
matches = []
params = {
    'region': 'NA'
}


@client.event
async def on_ready():
    """waits until the discord bot is online/active then starts the loop for get_data,
    if we don't wait it causes errors with getting the correct channel"""
    get_data.start()


@tasks.loop(minutes=10)
@client.event
async def get_data():
    channel = client.get_channel(id=939726187301863487)
    response = requests.get('https://api.vrmasterleague.com/EchoArena/Matches/History/Detailed', params=params)

    for match in response.json():
        division = match['homeTeam']['divisionName']

        if division == 'Master':
            match_ID = match['matchID']
            home_team = match['homeTeam']['teamName']
            away_team = match['awayTeam']['teamName']
            home_score = match['homeScore']
            away_score = match['awayScore']

            round_info = ''
            home_rounds = 0
            away_rounds = 0

            for round_ in match['mapsSet']:
                map_name = round_['mapName']
                home_round_score = round_['homeScore']
                away_round_score = round_['awayScore']
                round_info += f'{map_name} ({home_round_score}-{away_round_score})\n'

                if home_round_score > away_round_score:
                    home_rounds += 1
                else:
                    away_rounds += 1

            if home_rounds > away_rounds:
                win_or_loss = 'wins'
            else:
                win_or_loss = 'loses'

            round_total = f'{home_rounds}-{away_rounds}'
            score_total = f'{home_score}-{away_score}'
            match_header = f'**{home_team}** {win_or_loss} vs **{away_team}** ({round_total}) ({score_total})'

            if match_ID in matches:
                # the match has already been posted to discord
                pass
            else:
                # keep track of which match's info we've already seen/sent, so it doesn't send repeat messages
                matches.append(match_ID)
                match_info = f':book:\n{match_header}\n{round_info}'
                await channel.send(match_info)

print('Starting bot...')
client.run(token)
