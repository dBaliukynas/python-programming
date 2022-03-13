class Season:

    def __init__(self, name):
        self.name = name
        self.teams = {}

    def add_team(self, team):
        self.teams[team.name] = team



class Game:
    '''
    A class that represents EuroLeague's game.

    ...


    Methods
    -------

    '''
    def __init__(self, name, _round, team1, team2):
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
        self.team1 = team1
        self.team2 = team2


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
        self.leaderboard_position= leaderboard_position


    def add_player(self, player):
        self.players[player.fullname] = player

    def find_win_percentage(self):
        return round(self.wins / (self.wins + self.losses) * 100, 4)


    def count_players_value(self, val):
        try:
            players_values = {}
            for player in self.players.values():
                    
                value = getattr(player, val) 
                 
                if value in players_values:
                    players_values[value] += 1
                else:
                    players_values[value] = 1
                    
            return dict(sorted(players_values.items(), 
                               key=lambda item: item[1], reverse=True))
        except AttributeError:
            print(f'No such attribute as "{val}"')
    
    def find_furthest_number_player(self):

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

                

class GamePerformance:
    '''
    A class that represents EuroLeague's team's performance in a game.

    ...


    Methods
    -------

    '''
    def __init__(self, team, performance_index_rating,
                 points, two_point_percent):
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

Season1=Season('2021-22')
Season1.add_team(Team('Zenit St Petersburg', 14, 9, 6))
Season1.add_team(Team('Panathinaikos OPAP Athens', 7, 19, 17))
Season1.add_team(Team('Zalgiris Kaunas', 7, 20, 18))
Season1.teams['Zenit St Petersburg'].add_player(Player('Tyson', 'Carter', 1, 'USA', 'Guard',
                                                       1.0, 0.5, 1.2, 0.5, 0.0,
                                                       0.2))
Season1.teams['Zenit St Petersburg'].add_player(Player('Jordan', 'Loyd', 2, 'USA', 'Guard',
                                                       13.2, 4.0, 3.9, 1.0, 0.1,
                                                       14.4))
Season1.teams['Zalgiris Kaunas'].add_player(Player('Niels', 'Giffey', 0, 'Germany',
                                                   'Forward', 5.6, 2.6, 0.7, 0.5, 0.1,
                                                    4.7))
Season1.teams['Zalgiris Kaunas'].add_player(Player('Karolis', 'Lukosiunas', 44, 'Lithuania',
                                                   'Forward', 3.1, 0.8, 0.5, 0.3, 0.0,
                                                    0.9))
Season1.teams['Zalgiris Kaunas'].add_player(Player('Tai', 'Webster', 22, 'New Zealand',
                                                   'Guard', 4.6, 1.1, 1.8, 0.4, 0.1,
                                                    2.8))

print(Season1.teams['Zenit St Petersburg'].players['Tyson Carter'].__dict__)
print(f'{Season1.teams["Zenit St Petersburg"].name} : '\
      f'{Season1.teams["Zenit St Petersburg"].count_players_value("position")}')
print(Season1.teams['Zalgiris Kaunas'].count_players_value('nationality'))
print(Season1.teams['Zalgiris Kaunas'].find_furthest_number_player())
