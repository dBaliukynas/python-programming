class Game:
    '''
    A class that represents EuroLeague's game.

    ...


    Methods
    -------

    '''
    def __init__(self, name, _round, season):
        '''
        Parameters
        ----------
        name : str
            Game's name.
        round : int
            Game's round in season.
        season : str
            The season in which the game happened.
        '''

        self.name = name
        self.round = _round
        self.season = season


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

        self.name = name
        self.wins = wins
        self.losses= losses
        self.leaderboard_position= leaderboard_position

class Player:
    '''
    A class that represents EuroLeague's player.

    ...


    Methods
    -------

    '''
    def __init__(self, name, surname, team, position):
        '''
        Parameters
        ----------
        name : str
            Player's name.
        surname : str
            Player's surname.
        team : str
            Team's losses in season.
        leaderboard_position : int
            Team's position in season's leaderboard

        '''
        
        self.name = name
        self.surname = surname
        self.team = team
        self.position = position

Game1 = Game("Zenit St Petersburg vs Panathinaikos OPAP Athens", 29, "2021-22")
