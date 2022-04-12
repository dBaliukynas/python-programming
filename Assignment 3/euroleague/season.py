from euroleague.team import Team
from euroleague.game import Game


class Season:
    '''
    A class that represents EuroLeague's season.
    '''

    def __init__(self, name):
        '''
        Initialize values when an instance is created.
        Parameters
        ----------
        name : str
             Season's name
        '''

        self.name = name
        self.teams = {}
        self.games = {}

    def add_team(self, team):
        '''
        Add team's instance to season's instance dictionary.
        Parameters
        ----------
        team : object
            Team's object.
        '''
        self.teams[team.name] = team

    def add_game(self, game):
        '''
        Add game's instance to season's instance dictionary.
        Parameters
        ----------
        game : object
            Game's object.
        '''
        self.games[game.name] = game

    @classmethod
    def from_json(cls, season_dict):
        '''
        Create an instance from dictionary.
        Parameters
        ----------
        season_dict : dict
            Dictionary representing EuroLeague's season.
        Returns
        -------
        season: object
            Instance representing EuroLeague's season.
        '''
        season = cls(season_dict['name'])

        season.teams = {team['name']: Team.from_json(team)
                        for team in season_dict['teams'].values()}
        season.games = {game['name']: Game.from_json(game, season_teams=season.teams)
                        for game in season_dict['games'].values()}

        return season

    def find_best_players_by_value(self, attribute):
        '''
        Find best player from a season by given attribute.
        Parameters
        ----------
        attribute : str
            Specific name of player's value, i.e. "points", "assists", etc.
        Returns
        -------
        best_players: list
            A list of player instances.
        '''

        if attribute in ('name', 'surname', 'fullname', 'nationality', 'position'):
            raise AttributeError(f'''Attribute "{attribute}" is not supported.
 Supported attributes: "number", "points", "rebounds", "assists", "steals",
   "blocks", "performance_index_rating".''')

        best_players_in_team = []
        for team in self.teams.values():
            if len(team.players) == 0:
                continue

            best_players_in_team.extend(
                team.find_best_players_by_value(attribute))

        sorted_best_players = sorted(best_players_in_team, reverse=True,
                                     key=lambda item: getattr(item, attribute))

        best_value = getattr(sorted_best_players[0], attribute)

        best_players = [sorted_best_player for sorted_best_player in sorted_best_players
                        if getattr(sorted_best_player, attribute) == best_value]

        return best_players

    def find_highest_streak_teams(self, attribute):
        '''
        Find teams that has highest streak.
        Parameters
        ----------
        attribute : str
            Name of streak: "win_streak" or "loss_streak"
        Returns
        -------
        highest_streak_team: list
            A list of team instances.
        '''

        if attribute not in ('win_streak', 'loss_streak'):
            raise AttributeError(f'''Attribute "{attribute}" is not supported.
Supported attributes: "win_streak", "loss_streak".''')

        sorted_teams = sorted(self.teams.items(), reverse=True,
                              key=lambda item: getattr(item[1], attribute))

        highest_streak = getattr(sorted_teams[0][1], attribute)

        highest_streak_teams = [sorted_team[1] for sorted_team in sorted_teams
                                if getattr(sorted_team[1], attribute) == highest_streak]

        return highest_streak_teams
