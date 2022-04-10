import requests
from bs4 import BeautifulSoup
import re


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

# for team_hyperlink in team_hyperlinks:
#     print(team_hyperlink)

# print(team_hyperlinks[0])

# =============================================================================
# team_url = team_hyperlinks[0]
# team_html = requests.get(team_url)
# team_doc = BeautifulSoup(team_html.text, 'html.parser')
#
# # print(team_doc.prettify())
#
# team_name = team_doc.find('p', class_=re.compile('^club-info_name'))
#
# team_win_loss = team_doc.find_all('span', class_=re.compile('^club-info_param'))
# team_wins = team_win_loss[0].string
# team_losses = team_win_loss[1].string
# =============================================================================

standings_url = 'https://www.euroleaguebasketball.net/euroleague/standings/'
standings_html = requests.get(standings_url)
standings_doc = BeautifulSoup(standings_html.text, 'html.parser')
standings_team_names =  standings_doc.find_all('span',
                                    class_=re.compile('^complex-stat-table_mainClubName'))



for standings_team_name in standings_team_names:
    print(standings_team_name.text.replace('*', ''))


team_leaderboard_row_fragments = standings_doc.find_all('div',
                       class_=re.compile('^complex-stat-table_sticky'))

for team_leaderboard_row_fragment in team_leaderboard_row_fragments:
    for team_leaderboard_position_wrappers in team_leaderboard_row_fragment.contents:
        for team_leaderboard_position in team_leaderboard_position_wrappers.contents:
            if (re.match(r'^<span', str(team_leaderboard_position)) is not None
                and team_leaderboard_position.string.isnumeric()):

                print(team_leaderboard_position.string)
