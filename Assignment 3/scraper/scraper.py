#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
import time
import threading

from euroleague.season import Season
from euroleague.team import Team
from euroleague.player import Player
from instance_utils import file_operations as fo

start = time.perf_counter()


def create_season(base_url, team_limit):
    base_html = requests.get(base_url)
    base_doc = BeautifulSoup(base_html.text, 'html.parser')

    tournament_name = base_doc.find(
        'h4', class_=re.compile('^our-tournaments-item_title'))
    tournament_url = tournament_name.next_sibling.attrs['href']
    tournament_html = requests.get(base_url + tournament_url)
    tournament_doc = BeautifulSoup(tournament_html.text, 'html.parser')

    standings_url = base_url + tournament_doc.find('a', text='Standings', class_=re.compile(
        '^main-nav_link')).attrs['href']
    standings_html = requests.get(standings_url)
    standings_doc = BeautifulSoup(standings_html.text, 'html.parser')
    standings_team_names = standings_doc.find_all('span',
                                                  class_=re.compile('^complex-stat-table_mainClubName'))

    season_name = standings_doc.find(
        'p', class_=re.compile('^standings_filterValue'))
    season_name = season_name.string.split(', ')[1]

    season = Season(season_name)

    teams_url = base_url + \
        tournament_doc.find('a', text='Teams', class_=re.compile(
            '^main-nav_link')).attrs['href']

    teams_html = requests.get(teams_url)
    teams_doc = BeautifulSoup(teams_html.text, 'html.parser')
    teams_list_doc = teams_doc.find_all('a', class_=re.compile('^teams-card'))
    team_hyperlinks = [base_url +
                       team_doc.attrs['href'] for team_doc in teams_list_doc]

    team_leaderboard_positions = create_leaderboard_positions(
        standings_doc, standings_team_names, season)

    for index, team_hyperlink in enumerate(team_hyperlinks):
        if team_limit is not None and index >= team_limit:
            return season

        season.add_team(create_team(index, base_url,
                        team_hyperlink, team_leaderboard_positions, verbose=True))

    return season


def create_team(team_index,  base_url, team_hyperlink, team_leaderboard_positions, verbose=None):
    team_html = requests.get(team_hyperlink)
    team_doc = BeautifulSoup(team_html.text, 'html.parser')
    team_name = team_doc.find('p', class_=re.compile('^club-info_name'))
    team_name = team_name.string
    team_win_loss = team_doc.find_all(
        'span', class_=re.compile('^club-info_param'))
    if (team_name in team_leaderboard_positions):

        team_leaderboard_position = team_leaderboard_positions[team_name]
    else:
        team_leaderboard_position = None

    if (team_win_loss):
        team_wins = int(team_win_loss[0].string)
        team_losses = int(team_win_loss[1].string)
    else:
        team_wins = None
        team_losses = None

    players_list_doc = team_doc.find_all(
        'a', class_=re.compile('^game-roster-group-player_playerCard'))

    player_hyperlinks = [base_url + player_doc.attrs['href']
                         for player_doc in players_list_doc if '/teams/' not in player_doc.attrs['href']]

    team = Team(team_name, team_wins, team_losses, team_leaderboard_position)

    if verbose is not None:
        create_team_print(team_html, team_doc, team_name,
                          team_win_loss, team_wins, team_losses, team_leaderboard_position)

    for player_hyperlink in player_hyperlinks:
        global fail_count
   
        while True:
            try:
                team.add_player(create_player(player_hyperlink, verbose=True))
                break
            except AttributeError:
                if verbose is not None:
                    print("Player creation failed. Retrying...")
                    fail_count += 1
                    time.sleep(3)

    return team


def create_team_print(team_html, team_doc, team_name, team_win_loss, team_wins, team_losses, team_leaderboard_position):
    print('''+------+
| TEAM |
+------+''')
    print('---------------------------------------------------------------')
    print(f'HTTP Status Code: {team_html.status_code}\n')
    print('**********************************************')
    print(team_doc.find('p', class_=re.compile('^club-info_name')))
    if (team_wins):
        print(team_win_loss[0])

    if (team_losses):
        print(team_win_loss[1])
    print('**********************************************\n')
    print(f'Name: {team_name}')
    print(f'Wins: {team_wins}')
    print(f'Losses: {team_losses}')
    print(f'Leaderboard position: {team_leaderboard_position}')
    print('---------------------------------------------------------------\n\n')


def create_leaderboard_positions(standings_doc, standings_team_names, season):
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


def create_player(player_hyperlink, verbose=None):
    player_html = requests.get(player_hyperlink)
    player_doc = BeautifulSoup(player_html.text, 'html.parser')
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

    if verbose is not None:
        create_player_print(player_html, player_doc, player_name, player_surname, player_number, player_nationality, player_position,
                            player_points, player_rebounds, player_assists, player_steals, player_blocks,
                            player_performance_index_rating)

    return player


def create_player_print(player_html, player_doc, player_name, player_surname, player_number, player_nationality,
                        player_position, player_points, player_rebounds, player_assists, player_steals, player_blocks,
                        player_performance_index_rating):
    print('''+--------+
| PLAYER |
+--------+''')
    print('---------------------------------------------------------------')
    print(f'HTTP Status Code: {player_html.status_code}\n')
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


def main():
    base_url = 'https://www.euroleaguebasketball.net'
    # season = create_season(base_url)
    # fo.write_to_file([season], 'season.json')
    # print(json.dumps(s, default=lambda item: item.__dict__))

fail_count = 0
season = create_season('https://www.euroleaguebasketball.net', None)
fo.write_to_file([season], 'testing1.json', 'testing2.json')
testing = fo.convert_to_instances(fo.load_from_file('testing1.json'), vars())
if __name__ == '__main__':
    main()

finish = time.perf_counter()
print(f'Total time: {finish-start} seconds')
print(f'Failed: {fail_count} times')
