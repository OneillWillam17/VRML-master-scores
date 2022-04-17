import os
import discord
from dotenv import load_dotenv
from scrape import Scrape
from etherealscrape import Ethereal


scrape = Scrape()
ethereal = Ethereal()

master_matches = []
master_teams = ["Oceans", "Redshift", "Ignite", "Instinct", "Zen", "Ethereal", "Kangorillaz", "Anomaly", "Overkill", "Seattle Beholders"]
plain_txt_match = []

scrape.scrape_data()
ethereal.ethereal_scrape()

# checks if teams that played are in master_teams list and scores are available
for match in scrape.info:
    
    if match['Home team'] in master_teams and match['score'] != 'Scores not submitted yet':
        
        master_matches.append(match)


def match_info():
    """reformats info inside master matches, outputs as plain text with w/l"""
    for game in master_matches:
        
        home = game['Home team']
        score = game['score']
        away = game['Away team']

        # checks if home team won or lost
        score1_int = int(score[0:2])
        score2_int = int(score[5:7])
        
        if score1_int > score2_int:
            winloss = 'wins'
        else:
            winloss = "loses"
            
        global plain_txt_match
        plain_txt_match.append(f'{home} {winloss} vs {away} ({score})')
        
        print(plain_txt_match)


match_info()

# start of discord bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


# Discord client interactions
@client.event
async def on_message(message):
    """scans messages for '!scores' and prints latest master match scores"""

    if message.author == client.user:
        return

    if message.content == '!scores':
        await message.channel.send("Recent master matches: \n")
        
        for i in range(len(plain_txt_match)):
            await message.channel.send(plain_txt_match[i])

    if message.content == '!ethereal':
        await message.channel.send('WIP, probably missing some matches')
        for each in ethereal.info:
            
            eth_home = each['Home team']
            eth_score = each['score']
            eth_away = each['Away team']

            # checks if home team won or lost
            score1_int = int(eth_score[0:2])
            score2_int = int(eth_score[5:7])
            
            if score1_int > score2_int:
                winloss = 'wins'
            else:
                winloss = "loses"
                
            await message.channel.send(f'{eth_home} {winloss} vs {eth_away} ({eth_score})')


# runs discord bot
client.run(TOKEN)
