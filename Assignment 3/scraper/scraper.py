import requests
from bs4 import BeautifulSoup
import re
import time
import concurrent.futures

from euroleague.season import Season
from euroleague.team import Team
from euroleague.player import Player


class EuroLeagueScraper:
    '''
    A class that represents EuroLeague's scraper.
    '''

    player_creation_fails = 0
    team_creation_fails = 0

    def __init__(self, threading=True, team_limit=None, team_verbose=False, player_verbose=False, sleep_time=0):
        '''
        Initialize values when an instance is created.
        Parameters
        ----------
        threading : bool
            A boolean value that tells whether scraper should run with Thread Pool or without.
        team_limit : int
            An integer value that tells the maximum amount of teams that should be scraped.
        team_verbose : bool
            A boolean value that tells whether scraper should print out information about team creation.
        player_verbose : bool
            A boolean value that tells whether scraper should print out information about player creation.
        sleep_time : int
            An integer value that tells for how long scraper should sleep when a player or team creation is failed (in seconds).
        '''

        self.base_url = 'https://www.euroleaguebasketball.net'
        self.threading = threading
        self.team_limit = team_limit
        self.team_verbose = team_verbose
        self.player_verbose = player_verbose
        self.sleep_time = sleep_time
        self.player_creation_fails = 0
        self.team_creation_fails = 0

    def create_season(self):
        '''
        Create season instance.
        '''

        base_response = requests.get(self.base_url)
        base_doc = BeautifulSoup(base_response.text, 'html.parser')

        tournament_name = base_doc.find(
            'h4', class_=re.compile('^our-tournaments-item_title'))
        tournament_url = tournament_name.next_sibling.attrs['href']
        tournament_response = requests.get(self.base_url + tournament_url)
        tournament_doc = BeautifulSoup(tournament_response.text, 'html.parser')

        standings_url = self.base_url + tournament_doc.find('a', text='Standings', class_=re.compile(
            '^main-nav_link')).attrs['href']
        standings_response = requests.get(standings_url)
        standings_doc = BeautifulSoup(standings_response.text, 'html.parser')
        standings_team_names = standings_doc.find_all('span',
                                                      class_=re.compile('^complex-stat-table_mainClubName'))

        season_name = standings_doc.find(
            'p', class_=re.compile('^standings_filterValue'))
        season_name = season_name.string.split(', ')[1]

        season = Season(season_name)

        teams_url = self.base_url + \
            tournament_doc.find('a', text='Teams', class_=re.compile(
                '^main-nav_link')).attrs['href']

        teams_response = requests.get(teams_url)
        teams_doc = BeautifulSoup(teams_response.text, 'html.parser')
        teams_list_doc = teams_doc.find_all(
            'a', class_=re.compile('^teams-card'))
        team_hyperlinks = [self.base_url +
                           team_doc.attrs['href'] for team_doc in teams_list_doc]

        team_leaderboard_positions = self.create_leaderboard_positions(
            standings_doc, standings_team_names, season)

        def add_teams(index, team_hyperlink):
            '''
            Add team instances to season instance's dictionary.
            '''

            if self.team_limit is not None and index >= self.team_limit:
                return season

            max_attempts = 2
            attempts = 0

            while attempts < max_attempts:
                try:

                    season.add_team(self.create_team(
                        team_hyperlink, team_leaderboard_positions))
                    break
                except (AttributeError, IndexError):
                    time.sleep(self.sleep_time)
                    attempts += 1

                if attempts == 1:
                    self.team_creation_fails += 1
                    self.__class__.team_creation_fails += 1

                print(
                    f"Team creation has failed. Retrying... \nURL: {team_hyperlink}\n")

        if self.threading:
            with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
                for index, team_hyperlink in enumerate(team_hyperlinks):
                    executor.submit(add_teams, index, team_hyperlink)
        else:
            for index, team_hyperlink in enumerate(team_hyperlinks):
                add_teams(index, team_hyperlink)

        print(f'Player creation fails: {self.player_creation_fails}')
        print(f'Team creation fails: {self.team_creation_fails}\n')

        return season

    def create_team(self, team_hyperlink, team_leaderboard_positions):
        '''
        Create team instance.
        Parameters
        ----------
        team_hyperlink : str
            URL of team's page.
        team_leaderboard_positions : dict
            A dictionary of team leaderboard positions (team names as key and leaderboard position as value).
        '''

        team_response = requests.get(team_hyperlink)
        team_doc = BeautifulSoup(team_response.text, 'html.parser')
        
        team_name = team_doc.find('p', class_=re.compile('^club-info_name'))
        team_name = team_name.string
        team_win_loss = team_doc.find_all(
            'span', class_=re.compile('^club-info_param'))

        if team_name in team_leaderboard_positions:
            team_leaderboard_position = team_leaderboard_positions[team_name]
        else:
            team_leaderboard_position = None

        if team_win_loss:
            team_wins = int(team_win_loss[0].string)
            team_losses = int(team_win_loss[1].string)
        else:
            team_wins = None
            team_losses = None

        players_list_doc = team_doc.find_all(
            'a', class_=re.compile('^game-roster-group-player_playerCard'))

        player_hyperlinks = [self.base_url + player_doc.attrs['href']
                             for player_doc in players_list_doc if '/teams/' not in player_doc.attrs['href']]

        team = Team(team_name, team_wins, team_losses,
                    team_leaderboard_position)

        if self.team_verbose:
            self.print_team_creation_info(team_response, team_doc, team_name,
                                          team_win_loss, team_wins, team_losses, team_leaderboard_position)

        for player_hyperlink in player_hyperlinks:
            max_attempts = 2
            attempts = 0

            while attempts < max_attempts:
                try:
                    team.add_player(self.create_player(
                        player_hyperlink))
                    break
                except (AttributeError, IndexError):
                    time.sleep(self.sleep_time)
                    attempts += 1

                if attempts == 1:
                    self.player_creation_fails += 1
                    self.__class__.player_creation_fails += 1

                    print(
                        f"Player creation has failed. Retrying... \nURL: {player_hyperlink}\n")

        return team

    @staticmethod
    def print_team_creation_info(team_response, team_doc, team_name, team_win_loss, team_wins, team_losses, team_leaderboard_position):
        '''
        Print information about team creation.
        Parameters
        ----------
        team_response : class
            A response received from a request.
        team_doc : class
            A class that represents team's HTML document.
        team_name : str
            Team's name.
        team_win_loss : list
            List that has 2 values: team's wins and loss count.
        team_wins : int
           Team's win count.
        team_losses : int
            Team's loss count.
        team_leaderboard_position : int
            Team's position in a season.
        '''

        print('''+------+
| TEAM |
+------+''')
        print('---------------------------------------------------------------')
        print(f'HTTP Status Code: {team_response.status_code}\n')
        print('**********************************************')
        print(team_doc.find('p', class_=re.compile('^club-info_name')))
        if team_wins:
            print(team_win_loss[0])

        if team_losses:
            print(team_win_loss[1])
        print('**********************************************\n')
        print(f'Name: {team_name}')
        print(f'Wins: {team_wins}')
        print(f'Losses: {team_losses}')
        print(f'Leaderboard position: {team_leaderboard_position}')
        print('---------------------------------------------------------------\n\n')

    @staticmethod
    def create_leaderboard_positions(standings_doc, standings_team_names, season):
        '''
        Create a dictionary of leaderboard positions.
        Parameters
        ----------
        standings_doc : class
            A class that represents standings HTML document.
        standings_team_names : list
            List of team names.
        season : object
            Season's instance.
        '''

        team_leaderboard_positions = {}
        team_leaderboard_row_fragments = standings_doc.find_all('div',
                                                                class_=re.compile('^complex-stat-table_sticky'))

        for index, team_leaderboard_row_fragment in enumerate(team_leaderboard_row_fragments):
            if index != 0:
                team_leaderboard_position = team_leaderboard_row_fragment.contents[
                    0].contents[0].string
                team_leaderboard_positions.update({
                    standings_team_names[index-1].text.replace('*', '').rstrip(): team_leaderboard_position.string})

        return team_leaderboard_positions

    def create_player(self, player_hyperlink):
        '''
        Create player instance.
        Parameters
        ----------
        player_hyperlink : str
            URL of player's page.
        '''

        player_response = requests.get(player_hyperlink)
        player_doc = BeautifulSoup(player_response.text, 'html.parser')

        player_name = player_doc.find('span', class_=re.compile(
            '^hero-info_firstName')).string.title().strip()
        player_surname = player_doc.find('span', class_=re.compile(
            '^hero-info_lastName')).string.title().strip()
        player_number = int(player_doc.find('div', class_=re.compile(
            '^hero-info_numberBlock')).contents[1].string)
        player_nationality = player_doc.find(
            'span', class_=re.compile('^hero-info_key')).next_sibling.string
        player_position = player_doc.find(
            'div', class_=re.compile('^hero-info_position')).string
        player_points = float(player_doc.find_all('span', text='PTS', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling.string)
        player_rebounds = float(player_doc.find_all('span', text='REB', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling.string)
        player_assists = float(player_doc.find_all('span', text='AST', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling.string)
        player_steals = float(player_doc.find_all('span', text='STL', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling.string)
        player_blocks = float(player_doc.find_all('span', text='BLK', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling.string)
        player_performance_index_rating = float(player_doc.find_all('span', text='PIR', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling.string)

        player = Player(player_name, player_surname, player_number, player_nationality, player_position, player_points,
                        player_rebounds, player_assists, player_steals, player_blocks, player_performance_index_rating)

        if self.player_verbose:
            self.print_player_creation_info(player_response, player_doc, player_name, player_surname, player_number, player_nationality, player_position,
                                            player_points, player_rebounds, player_assists, player_steals, player_blocks,
                                            player_performance_index_rating)

        return player

    @staticmethod
    def print_player_creation_info(player_response, player_doc, player_name, player_surname, player_number, player_nationality,
                                   player_position, player_points, player_rebounds, player_assists, player_steals, player_blocks,
                                   player_performance_index_rating):
        '''
        Print information about player creation.
        Parameters
        ----------
        player_response : class
            A response received from a request.
        player_doc : class
            A class that represents player HTML document.
        player_name : str
            Player's name.
        player_surname : str
            Player's surname.
        player_number : int
            Player's number.
        player_nationality : str
            Player's nationality.
        player_position : str
            Player's position.
        player_points : float
            Player's points.
        player_rebounds : float
            Player's rebounds.
        player_assists : float
            Player's assists.
        player_steals : float
            Player's steals.
        player_blocks : float
            Player's blocks.
        player_performance_index_rating : float
            Player's performance index rating.
        '''
        print('''+--------+
    | PLAYER |
    +--------+''')
        print('---------------------------------------------------------------')
        print(f'HTTP Status Code: {player_response.status_code}\n')
        print('**********************************************')
        print(player_doc.find('span', class_=re.compile('^hero-info_firstName')))
        print(player_doc.find('span', class_=re.compile('^hero-info_lastName')))
        print(player_doc.find('div', class_=re.compile(
            '^hero-info_numberBlock')).contents[1])
        print(player_doc.find(
            'span', class_=re.compile('^hero-info_key')).next_sibling)
        print(player_doc.find(
            'div', class_=re.compile('^hero-info_position')))
        print(player_doc.find_all('span', text='PTS', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling)
        print(player_doc.find_all('span', text='REB', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling)
        print(player_doc.find_all('span', text='AST', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling)
        print(player_doc.find_all('span', text='STL', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling)
        print(player_doc.find_all('span', text='BLK', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling)
        print((player_doc.find_all('span', text='PIR', class_=re.compile(
            '^stats-item_name'))[0].previous_sibling))

        print('**********************************************\n')
        print(player_name, player_surname)
        print(f'Number: {player_number}')
        print(f'Nationality: {player_nationality}')
        print(f'Position: {player_position}')
        print(f'Points: {player_points}')
        print(f'Rebounds: {player_rebounds}')
        print(f'Assists: {player_assists}')
        print(f'Steals: {player_steals}')
        print(f'Blocks: {player_blocks}')
        print(f'Performance Index Rating: {player_performance_index_rating}')
        print('---------------------------------------------------------------\n\n')
