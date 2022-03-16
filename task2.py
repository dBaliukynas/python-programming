import sys
import json

class Season:

    def __init__(self, name):
        self.name = name
        self.teams = {}

    def add_team(self, team):
        self.teams[team.name] = team
        
    @classmethod
    def from_json(cls, season_dict):
        season = cls(season_dict['name'])
        
        
        season.teams = {team['name']:Team.from_json(
            team['players'],
            team['name'],
            team['wins'], 
            team['losses'], 
            team['leaderboard_position']
            ) 
             for team in season_dict['teams'].values()}
            
        return season
        

    def find_best_player_by_value(self, attribute):
        best_players_in_team = []
        for team in self.teams.values():
            if len(team.players) == 0:
                continue
            best_players_in_team.append(team.find_best_player_by_value(attribute))
            
        return sorted(best_players_in_team, reverse=True,
                      key=lambda item: getattr(list(item.values())[0], attribute))
    
    def find_highest_streak_team(self, attribute):
        if attribute not in ('win_streak', 'loss_streak'):
            print(f'''Attribute "{attribute}" is not supported. 
Supported attributes: "win_streak", "loss_streak".''')
            sys.exit()
        
        sorted_teams = sorted(self.teams.items(), reverse=True,
                              key=lambda item: getattr(item[1], attribute))
       
        highest_streak = getattr(sorted_teams[0][1], attribute)
        
        return dict([sorted_team for sorted_team in sorted_teams
          if getattr(sorted_team[1], attribute) == highest_streak])
            

class Game:
    '''
    A class that represents EuroLeague's game.

    ...


    Methods
    -------

    '''
    def __init__(self, name, _round, team1_performance, team2_performance):
        '''
        Parameters
        ----------
        name : str
            Game's name.
        round : int
            Game's round in season.
        '''

        self.name = name
        self.round = _round
        self.team1_performance = team1_performance
        self.team2_performance = team2_performance
        
        def add_streak(self):
            if self.team1_performance.points > self.team2_performance.points:
                self.team1_performance.team.win_streak += 1
                self.team2_performance.team.win_streak = 0
                self.team2_performance.team.loss_streak += 1
                
            else:
                self.team2_performance.team.win_streak += 1
                self.team1_performance.team.win_streak = 0
                self.team1_performance.team.loss_streak += 1
    
        
        add_streak(self)
        
    def count_performance_difference(self):
        team_performance_difference = {self.team1_performance.team: {}}
        team_performance_attributes =  ([attribute for attribute in (dir(self.team1_performance)) 
         if not attribute.startswith('__') and not attribute.endswith('__') 
                                           and attribute != 'team'])
        for team_performance_attribute in team_performance_attributes:
            team1_attribute = getattr(self.team1_performance, 
                                      team_performance_attribute)
            team2_attribute = getattr(self.team2_performance, 
                                      team_performance_attribute)
            
                
            team_performance_difference[self.team1_performance.team].update(
            {team_performance_attribute : round(team1_attribute - team2_attribute, 2)})
            
        return team_performance_difference
    
    def find_better_team_by_value(self, attribute):
        try:
            team1_value = getattr(self.team1_performance, attribute)
            team2_value = getattr(self.team2_performance, attribute)
            if team1_value > team2_value:
                return self.team1_performance.team
            return self.team2_performance.team
        except AttributeError:
            print(f'No such attribute as "{attribute}".')
            sys.exit()
        
            


class Team:
    '''
    A class that represents EuroLeague's team.

    ...


    Methods
    -------

    '''
    def __init__(self, name, wins, losses, leaderboard_position):
        '''
        Parameters
        ----------
        name : str
            Team's name.
        wins : int
            Team's wins in season.
        losses : int
            Team's losses in season.
        leaderboard_position : int
            Team's position in season's leaderboard

        '''

        self.players = {}
        self.name = name
        self.wins = wins
        self.losses= losses
        self.win_streak = 0
        self.loss_streak = 0
        self.leaderboard_position = leaderboard_position
        
    @classmethod
    def from_json(cls, players, name, wins, losses,
                  leaderboard_position):
        team = cls(name, wins, losses, leaderboard_position)
        team.win_streak = 0
        team.loss_streak = 0
        
        team.players = {player['name']:Player.from_json(
            player['name'], 
            player['surname'], player['number'],
            player['nationality'], player['position'],
            player['points'], player['rebounds'],
            player['assists'], player['steals'],
            player['blocks'], player['performance_index_rating']
            )
             for player in players.values()}
        return team


    def add_player(self, player):
        self.players[player.fullname] = player

    def find_win_percentage(self):
        return round(self.wins / (self.wins + self.losses) * 100, 4)


    def count_players_value(self, attribute):
        try:
            if attribute not in ('name', 'surname', 'nationality', 'position'):
                print(f'''Attribute "{attribute}" is not supported. 
Supported attributes: "name", "surname", "nationality", "position".''')
                sys.exit()
            players_values = {}
            for player in self.players.values():
                    
                value = getattr(player, attribute) 
                 
                if value in players_values:
                    players_values[value] += 1
                else:
                    players_values[value] = 1
                    
            return dict(sorted(players_values.items(), 
                               key=lambda item: item[1], reverse=True))
        except AttributeError:
            print(f'No such attribute as "{attribute}".')
            sys.exit()
    
    def find_furthest_number_players(self):

        number_diff = []
        sorted_players = (sorted(self.players.items(), key=lambda item: item[1].number))
       
        for index in range(len(sorted_players)):
            if index == 0 and len(sorted_players) != 1:
                number_diff.append(sorted_players[index + 1][1].number - sorted_players[index][1].number)
            elif index < len(sorted_players) - 1:
                
                number_diff.append(min(sorted_players[index + 1][1].number - sorted_players[index][1].number, 
                          sorted_players[index][1].number - sorted_players[index - 1][1].number))
            else:
                number_diff.append((sorted_players[index][1].number - sorted_players[index - 1][1].number))
    
        
     
        return dict(sorted_players[0:len([index for index, number in
                                       enumerate(number_diff) if number == max(number_diff)])])
    
    def find_best_player_by_value(self, attribute):
        sorted_players = sorted(self.players.items(), 
                               key=lambda item: getattr(item[1], attribute), 
                               reverse=True)
        
        best_value = getattr(sorted_players[0][1], attribute)
   
        return dict([sorted_player for sorted_player in sorted_players
                if getattr(sorted_player[1], attribute) == best_value])

                

class TeamPerformance:
    '''
    A class that represents EuroLeague's team's performance in a game.

    ...


    Methods
    -------

    '''
    def __init__(self, team, performance_index_rating, points, two_point_percent,
                 three_point_percent, free_throw_percent, offensive_rebounds,
                 defensive_rebounds, assists, steals, blocks, turnovers):
        '''
        Parameters
        ----------
        team : object
            Team.
        performance_index_rating : int
            Team's wins in season.
        index_rating : int
            Team's losses in season.
        two_point_percent : float
            Team's position in season's leaderboard

        '''

        self.team = team
        self.performance_index_rating = performance_index_rating
        self.points = points
        self.two_point_percent = two_point_percent
        self.three_point_percent = three_point_percent
        self.free_throw_percent = free_throw_percent
        self.offensive_rebounds = offensive_rebounds
        self.defensive_rebounds = defensive_rebounds
        self.assists = assists
        self.steals = steals
        self.blocks = blocks
        self.turnovers = turnovers

class Player:
    '''
    A class that represents EuroLeague's player.

    ...


    Methods
    -------

    '''
    def __init__(self, name, surname, number, nationality, position,
                 points, rebounds, assists, steals, blocks,
                 performance_index_rating):
        '''
        Parameters
        ----------
        name : str
            Player's name.
        surname : str
            Player's surname.
        position : str
            Player's position, i.e. Guard, Forward, etc.

       '''

        self.name = name
        self.surname = surname
        self.fullname = name + ' ' + surname
        self.number = number
        self.nationality = nationality
        self.position = position
        self.points = points
        self.rebounds = rebounds
        self.assists = assists
        self.steals = steals
        self.blocks = blocks
        self.performance_index_rating = performance_index_rating
        
    @classmethod
    def from_json(cls, name, surname, number, nationality, position,
                  points, rebounds, assists, steals, blocks,
                  performance_index_rating):
        player = cls(name, surname, number, nationality, position,
                      points, rebounds, assists, steals, blocks,
                      performance_index_rating)
        player.fullname = player.name + ' ' + surname
        
        return player

# Season1 = Season('2021-22')
# Season1.add_team(Team('Zenit St Petersburg', 14, 9, 6))
# Season1.add_team(Team('Panathinaikos OPAP Athens', 7, 19, 17))
# Season1.add_team(Team('Zalgiris Kaunas', 7, 20, 18))
# Season1.add_team(Team('FC Barcelona', 21, 6, 1))
# Season1.teams['Zenit St Petersburg'].add_player(Player('Tyson', 'Carter', 1, 'USA', 'Guard',
#                                                         1.0, 0.5, 1.2, 0.5, 0.0,
#                                                         0.2))
# Season1.teams['Zenit St Petersburg'].add_player(Player('Jordan', 'Loyd', 2, 'USA', 'Guard',
#                                                         13.2, 4.0, 3.9, 1.0, 0.1,
#                                                         14.4))
# Season1.teams['Zalgiris Kaunas'].add_player(Player('Niels', 'Giffey', 3, 'Germany',
#                                                     'Forward', 5.6, 2.6, 0.7, 0.5, 0.1,
#                                                     4.7))
# Season1.teams['Zalgiris Kaunas'].add_player(Player('Karolis', 'Lukosiunas', 1, 'Lithuania',
#                                                     'Forward', 3.1, 0.8, 0.5, 0.3, 0.0,
#                                                     0.9))
# Season1.teams['Zalgiris Kaunas'].add_player(Player('Tai', 'Webster', 12, 'New Zealand',
#                                                     'Guard', 4.6, 1.1, 1.8, 0.4, 0.1,
#                                                     2.8))

# print(Season1.teams['Zenit St Petersburg'].players['Tyson Carter'].__dict__)
# print(f'{Season1.teams["Zenit St Petersburg"].name} : '\
      # f'{Season1.teams["Zenit St Petersburg"].count_players_value("position")}')
# print(Season1.teams['Zalgiris Kaunas'].count_players_value('nationality'))
# print(Season1.teams['Zalgiris Kaunas'].find_furthest_number_players())

# =============================================================================
# Game1 = Game('Zalgiris Kaunas vs FC Barcelona', 29, 
#              TeamPerformance(Season1.teams['Zalgiris Kaunas'], 108, 91, 44.2, 42.9,
#                              85.4, 11, 17, 13, 13, 5, 12),
#              TeamPerformance(Season1.teams['FC Barcelona'], 71, 84, 53.8, 40.0,
#                              87.0, 11, 23, 20, 1, 0, 22 ))
# Game1 = Game('Zalgiris Kaunas vs FC Barcelona', 29, 
#              TeamPerformance(Season1.teams['FC Barcelona'], 108, 91, 44.2, 42.9,
#                              85.4, 11, 17, 13, 13, 5, 12),
#              TeamPerformance(Season1.teams['Zenit St Petersburg'], 71, 84, 53.8, 40.0,
#                              87.0, 11, 23, 20, 1, 0, 22 ))
# =============================================================================
# print(Game1.team1_performance.__dict__)
print('\n')
# print(Game1.count_performance_difference())
# print(Game1.find_better_team_by_value('assists'))
# print(Season1.find_best_player_by_value('assists'))
# print(Season1.find_highest_streak_team('win_streak'))
def object_decoder(obj):
  
    return Season(obj)


    
# with open('instances.txt', 'w') as file:
#     json.dump(Season1, file, default=lambda x: x.__dict__)
    
# print(instances['Season1'])
with open('instances.txt') as file:
    season1 = json.load(file)
# season1 = Season.from_json(season1)
# Sea = Season(**test)
# Season.from_json(test)
# print(Sea.teams)
season1 = Season.from_json(season1)
print(season1)


