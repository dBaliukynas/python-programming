from euroleague.team import Team

class TeamPerformance:
    '''
    A class that represents EuroLeague's team's performance in a game.
    '''
    def __init__(self, team, performance_index_rating, points, two_point_percent,
                 three_point_percent, free_throw_percent, offensive_rebounds,
                 defensive_rebounds, assists, steals, blocks, turnovers):
        '''
        Initialize values when an instance is created.
        Parameters
        ----------
        team : object
            Team.
        performance_index_rating : int
            Team's performance index rating.
        points : int
            Team's points.
        two_point_percent : float
            Team's two-point accuracy in percent.
        three_point_percent : float
            Team's three-point accuracy in percent.
        free_throw_percent : float
            Team's free throw accuracy in percent.
        offensive_rebounds : int
            Team's offensive rebounds.
        defensive_rebounds : int
            Team's defensive rebounds.
        assists : int
            Team's assists.
        steals : int
            Team's steals.
        blocks : int
            Team's blocks.
        turnovers : int
            Team's turnovers.
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


    @classmethod
    def from_json(cls, team_performance_dict, season_teams={}):
        '''
        Create an instance from dictionary.
        Parameters
        ----------
        team_performance_dict : dict
            Dictionary representing EuroLeague's team's performance.
        season_teams : dict
            All teams in a season.
        Returns
        -------
        team_performance: object
            Instance representing EuroLeague's team's performance.
        '''
        if season_teams:
            for season_team_name, season_team in season_teams.items():
                if team_performance_dict['team']['name'] == season_team_name:
                    team = season_team
        else:
            team = Team.from_json(team_performance_dict['team'])
        team_performance = cls(team, team_performance_dict['performance_index_rating'],
                               team_performance_dict['points'],
                               team_performance_dict['two_point_percent'],
                               team_performance_dict['three_point_percent'],
                               team_performance_dict['free_throw_percent'],
                               team_performance_dict['offensive_rebounds'],
                               team_performance_dict['defensive_rebounds'],
                               team_performance_dict['assists'],
                               team_performance_dict['steals'],
                               team_performance_dict['blocks'],
                               team_performance_dict['turnovers'])

        return team_performance
