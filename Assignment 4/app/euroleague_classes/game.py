from app.euroleague_classes.team_performance import TeamPerformance

class Game:
    '''
    A class that represents EuroLeague's game.
    '''
    def __init__(self, name, _round, team1_performance, team2_performance):
        '''
        Initialize values when an instance is created.
        Parameters
        ----------
        name : str
            Game's name.
        round : int
            Game's round.
        team1_performance : object
            Team's that is participating in game performance instance.
        team2_performance : object
            Team's that is participating in game performance instance.
        '''

        self.name = name
        self.round = _round
        self.team1_performance = team1_performance
        self.team2_performance = team2_performance

        def add_streak(self):
            '''
            Add streak to team whenever game instance is created.
            '''

            if self.team1_performance.points > self.team2_performance.points:
                self.team1_performance.team.win_streak = 1
                self.team2_performance.team.win_streak = 0
                self.team1_performance.team.loss_streak = 0
                self.team2_performance.team.loss_streak += 1

            else:
                self.team2_performance.team.win_streak += 1
                self.team1_performance.team.win_streak = 0
                self.team2_performance.team.loss_streak = 0
                self.team1_performance.team.loss_streak += 1


        add_streak(self)

    @classmethod
    def from_json(cls, game_dict, season_teams={}):
        '''
        Create an instance from dictionary.
        Parameters
        ----------
        game_dict : dict
            Dictionary representing EuroLeague's game.
        season_teams : dict
            All teams in a season.
        Returns
        -------
        game: object
            Instance representing EuroLeague's game.
        '''

        team1_performance = TeamPerformance.from_json(game_dict['team1_performance'],
                                                      season_teams=season_teams)
        team2_performance = TeamPerformance.from_json(game_dict['team2_performance'],
                                                      season_teams=season_teams)
        game = cls(game_dict['name'], game_dict['round'], team1_performance,
                   team2_performance)

        return game

    def count_performance_difference(self):
        '''
        Count all team's performance values differences.
        Returns
        -------
        team_performance_difference: dict
            A dictionary of team performance values differences.
        '''

        team_performance_difference = {self.team1_performance.team: {}}
        team_performance_attributes =  ([attribute for attribute
                                         in (dir(self.team1_performance))
         if not attribute.startswith('__') and not attribute.endswith('__')
                                           and attribute not in ('team',
                                                                 'from_json')])

        for team_performance_attribute in team_performance_attributes:
            team1_attribute = getattr(self.team1_performance,
                                      team_performance_attribute)
            team2_attribute = getattr(self.team2_performance,
                                      team_performance_attribute)


            team_performance_difference[self.team1_performance.team].update(
            {team_performance_attribute : round(team1_attribute - team2_attribute, 2)})

        return team_performance_difference

    def find_better_team_by_value(self, attribute):
        '''
        Find team that has higher value than the other.
        Parameters
        ----------
        attribute : str
            Specific name of team's performance value, i.e.
            "points", "assists", etc.
        Returns
        -------
        object
            A team performance instance.
        '''

        team1_value = getattr(self.team1_performance, attribute)
        team2_value = getattr(self.team2_performance, attribute)
        if team1_value > team2_value:
            return self.team1_performance.team
        if team1_value == team2_value:
            return None
        return self.team2_performance.team
