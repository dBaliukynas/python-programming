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
        return round(self.wins / (self.wins + self.losses) * 100, 2)

    def count_players_positions(self):
        guard_count = 0
        forward_count = 0
        center_count = 0
        coach_count = 0
        for player in self.players.values():
            if player.position == 'Guard':
                guard_count += 1
            elif player.position == 'Forward':
                forward_count += 1
            elif player.position == 'Center':
                center_count += 1
            else:
                coach_count += 1

        return {
            'Guard': guard_count,
            'Forward': forward_count,
            'Center': center_count,
            'Coach': coach_count
            }


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
    def __init__(self, name, surname, position,
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
Season1.teams['Zenit St Petersburg'].add_player(Player('Tyson', 'Carter', 'Guard',
                                                       1.0, 0.5, 1.2, 0.5, 0.0,
                                                       0.2))
Season1.teams['Zenit St Petersburg'].add_player(Player('Jordan', 'Loyd', 'Guard',
                                                       13.2, 4.0, 3.9, 1.0, 0.1,
                                                       14.4))
# Season1.teams[0].add_player(Player('Tyson', 'Carter', 'Guard'))
# Season1.teams[0].add_player(Player('Tyson', 'Carter', 'Guard'))
print(Season1.teams['Zenit St Petersburg'].players['Jordan Loyd'].__dict__)
print(Season1.teams['Zenit St Petersburg'].count_players_positions())
