#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re

from euroleague.season import Season
from euroleague.team import Team
# def main():

teams_url = 'https://www.euroleaguebasketball.net/euroleague/teams/'
teams_html = requests.get(teams_url)
teams_doc = BeautifulSoup(teams_html.text, 'html.parser')

# print(html.prettify())
# teams_list_doc = teams_doc.find(class_='teams-list_list__3M_EG')
teams_list_doc = teams_doc.find('ul', class_=re.compile('^teams-list'))
# teams_list_doc = teams_doc.select('ul[class*="teams-list"]')
# print(teams_list_doc)
# print(teams_list_doc)
# print(teams_list_doc.contents)

team_hyperlinks = ['https://www.euroleaguebasketball.net/' + \
    list(team_doc.children)[0].attrs['href'] for team_doc in teams_list_doc.contents]


standings_url = 'https://www.euroleaguebasketball.net/euroleague/standings/'
standings_html = requests.get(standings_url)
standings_doc = BeautifulSoup(standings_html.text, 'html.parser')
standings_team_names =  standings_doc.find_all('span',
                                    class_=re.compile('^complex-stat-table_mainClubName'))

season_name = standings_doc.find('p', class_=re.compile('^standings_filterValue'))
season_name = season_name.string.split(', ')[1]

season_1 = Season(season_name)



for team_hyperlink in team_hyperlinks:
    team_html = requests.get(team_hyperlink)
    team_doc = BeautifulSoup(team_html.text, 'html.parser')
    team_name = team_doc.find('p', class_=re.compile('^club-info_name'))
    team_name = team_name.string
    team_win_loss = team_doc.find_all('span', class_=re.compile('^club-info_param'))

    # print(team_win_loss)
    if (team_win_loss):
        team_wins = int(team_win_loss[0].string)
        team_losses = int(team_win_loss[1].string)
    else:
        team_wins = None
        team_losses = None

    season_1.add_team(Team(team_name, team_wins, team_losses))

    team_leaderboard_row_fragments = standings_doc.find_all('div',
                           class_=re.compile('^complex-stat-table_sticky'))

for index, team_leaderboard_row_fragment in enumerate(team_leaderboard_row_fragments):
    for team_leaderboard_position_wrappers in team_leaderboard_row_fragment.contents:
        for team_leaderboard_position in team_leaderboard_position_wrappers.contents:
            if (re.match(r'^<span', str(team_leaderboard_position)) is not None
                and team_leaderboard_position.string.isnumeric()):
                season_1.teams[standings_team_names[index-1].text.replace('*', '').rstrip()] \
                    .leaderboard_position = int(team_leaderboard_position.string)

s = season_1.__dict__

# if __name__ == '__main__':
#     main()
