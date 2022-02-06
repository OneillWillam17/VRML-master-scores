import requests
from bs4 import BeautifulSoup


class Scrape:

    def __init__(self):
        """on init, save URL of VRML to be scraped and create empty list for match info """
        self.URL = 'https://vrmasterleague.com/EchoArena/Matches/vjOaUp4JlmG7C2Cl_fVZmQ2'
        self.info = []

    def scrape_data(self):
        """"Scrapes data from VRML website and saves it to scrape.info list"""
        website = requests.get(self.URL)

        soup = BeautifulSoup(website.content, 'html.parser')

        # results = soup.find('tbody', class_='tbody-has-headliners')

        matches = soup.find_all('tr', class_='vrml_table_row matches_team_row')

        # Loops over matches in table, pulls names of teams and score from past matches. Saves them to self.info
        for match in matches:
            # finds the home team's name
            home_team = match.find('td', class_='home_team_cell')
            home_team_name = home_team.find('span', class_='team_name')

            # finds the away's team name
            away_team = match.find('td', class_='away_team_cell')
            away_team_name = away_team.find('span', class_='team_name')

            # simplifies the text in both names
            home_team_plain = home_team_name.text.strip()
            away_team_plain = away_team_name.text.strip()

            # finds score of home vs away
            score = match.find('div', class_='match-set-wrapper')

            # attempts to save score to plain text
            try:
                plain_text_score = score.text
            except AttributeError:
                plain_text_score = 'Scores not submitted yet'

            # adds the names and score to list as dictionary
            self.info.append(
                {
                 'Home team': home_team_plain,
                 'Away team': away_team_plain,
                 'score': plain_text_score
                 }
            )

    def clear_data(self):
        """clears the existing match info"""
        self.info = []