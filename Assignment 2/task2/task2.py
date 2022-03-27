import json

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

        season.teams = {team['name']:Team.from_json(team)
                        for team in season_dict['teams'].values()}
        season.games = {game['name']:Game.from_json(game, season.teams)
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
            raise AttributeError( f'''Attribute "{attribute}" is not supported.
 Supported attributes: "number", "points", "rebounds", "assists", "steals",
   "blocks", "performance_index_rating".''')


        best_players_in_team = []
        for team in self.teams.values():
            if len(team.players) == 0:
                continue

            best_players_in_team.extend(team.find_best_players_by_value(attribute))

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
                self.team1_performance.team.win_streak += 1
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
    def from_json(cls, game_dict, season_teams):
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
                                                      season_teams)
        team2_performance = TeamPerformance.from_json(game_dict['team2_performance'],
                                                      season_teams)
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



class Team:
    '''
    A class that represents EuroLeague's team.
    Methods
    -------
    find_furthest_number_player()
        Find a player in team whose number is furthest
        from adjacent player numbers.
    '''

    def __init__(self, name, wins, losses, leaderboard_position):
        '''
        Initialize values when an instance is created.
        Parameters
        ----------
        players : dict
            Team's players.
        name : str
            Team's name.
        wins : int
            Team's wins.
        losses : int
            Team's losses.
        leaderboard_position : int
            Team's position in leaderboard.
        '''

        self.players = {}
        self.name = name
        self.wins = wins
        self.losses= losses
        self.win_streak = 0
        self.loss_streak = 0
        self.leaderboard_position = leaderboard_position

    @classmethod
    def from_json(cls, team_dict):
        '''
        Create an instance from dictionary.
        Parameters
        ----------
        team_dict : dict
            Dictionary representing EuroLeague's team.
        Returns
        -------
        team: object
            Instance representing EuroLeague's team.
        '''

        team = cls(team_dict['name'], team_dict['wins'], team_dict['losses'],
                   team_dict['leaderboard_position'])
        team.win_streak = 0
        team.loss_streak = 0

        team.players = {player['name'] + ' ' + player['surname']:Player.from_json(player)
             for player in team_dict['players'].values()}
        return team




    def add_player(self, player):
        '''
        Add player to team's instance dictionary.
        Parameters
        ----------
        player : object
            Instance representing EuroLeague's player.
        '''

        self.players[player.fullname] = player

    def find_win_percentage(self):
        '''
        Find team's win percentage.
        Returns
        -------
        float
            A float that represents team's win percentage.
        '''

        return round(self.wins / (self.wins + self.losses) * 100, 4)


    def count_players_value(self, attribute):
        '''
        Count players values by given attribute.
        Parameters
        ----------
        team_dict : dict
            Specific name of player's value, i.e.
            "nationality", "position", etc.
        Returns
        -------
        dict
            Sorted dictionary in descending order,
            containing keys as attributes and values as players values.
        '''

        if attribute not in ('name', 'surname', 'nationality', 'position'):
            raise AttributeError(f'''Attribute "{attribute}" is not supported.
Supported attributes: "name", "surname", "nationality", "position".''')

        players_values = {}
        for player in self.players.values():

            value = getattr(player, attribute)

            if value in players_values:
                players_values[value] += 1
            else:
                players_values[value] = 1

        return dict(sorted(players_values.items(),
                           key=lambda item: item[1], reverse=True))


    def find_furthest_number_players(self):
        '''
        Find players whose numbers are
        furhtest from other adjacent player numbers.
        Returns
        -------
        furthest_number_players : list
           List of sorted players by number whose
           number is furthest from other adjacent player numbers.
        '''

        number_diff = []
        sorted_players = (sorted(self.players.values(), key=lambda item: item.number))

        for index in range(len(sorted_players)):
            if index == 0 and len(sorted_players) != 1:
                number_diff.append(sorted_players[index + 1].number
                                   - sorted_players[index].number)
            elif index < len(sorted_players) - 1:

                number_diff.append(min(
                  (sorted_players[index].number - sorted_players[index - 1].number),
                  (sorted_players[index + 1].number -
                   sorted_players[index].number )))
            else:
                number_diff.append((sorted_players[index].number -
                                    sorted_players[index - 1].number) )

        furthest_number_players = sorted_players[number_diff.index(max(number_diff)):
                              len([index for index, number in
                                   enumerate(number_diff) if number
                                   == max(number_diff)])+number_diff.index(max(number_diff))]

        return furthest_number_players


    def find_best_players_by_value(self, attribute):
        '''
        Find best player from a team by given attribute.
        Parameters
        ----------
        attribute : str
            Specific name of player's value, i.e. "points", "assists", etc.
        Returns
        -------
        list
            A list of player instances.
        '''

        sorted_players = sorted(self.players.items(),
                               key=lambda item: getattr(item[1], attribute),
                               reverse=True)

        best_value = getattr(sorted_players[0][1], attribute)

        return [sorted_player[1] for sorted_player in sorted_players
                if getattr(sorted_player[1], attribute) == best_value]



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
    def from_json(cls, team_performance_dict, season_teams):
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

        for season_team_name, season_team in season_teams.items():
            if team_performance_dict['team']['name'] == season_team_name:
                team = season_team
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



class Player:
    '''
    A class that represents EuroLeague's player.
    '''
    def __init__(self, name, surname, number, nationality, position,
                 points, rebounds, assists, steals, blocks,
                 performance_index_rating):
        '''
        Initialize values when an instance is created.
        Parameters
        ----------
        name : str
            Player's name.
        surname : str
            Player's surname.
        number : int
            Player's number.
        nationality : str
            Player's nationality.
        position : str
            Player's position, i.e. Guard, Forward, etc.
        points : float
            Player's points (PTS) in a single season.
        rebounds : float
            Player's rebounds (REB) in a single season.
        assists : float
            Player's assists (AST) in a single season.
        steals : float
            Player's steals (STL) in a single season.
        blocks : float
            Player's blocks (BLK) in a single season.
        performance_index_rating : float
            Player's performance index rating (PIR) in a single season.
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
    def from_json(cls, player_dict):
        '''
        Create an instance from dictionary.
        Parameters
        ----------
        player_dict : dict
            Dictionary representing EuroLeague's player.
        Returns
        -------
        player object
            Instance representing EuroLeague's player.
        '''

        player = cls(player_dict['name'], player_dict['surname'],
                     player_dict['number'],
                     player_dict['nationality'],
                     player_dict['position'], player_dict['points'],
                     player_dict['rebounds'],
                     player_dict['assists'], player_dict['steals'],
                     player_dict['blocks'],
                     player_dict['performance_index_rating'])

        player.fullname = player.name + ' ' + player.surname

        return player

def write_to_file(instance):
    '''
    Write instance to file in dictionary structure.
    Parameters
    ----------
    instance : obj
        Instance.
    '''

    with open('instances.txt', 'w') as file:
        json.dump(instance, file, default=lambda item: item.__dict__)

def load_from_file():
    '''
    Load dictionaries from file that represent instances.
    Returns
    ----------
    dict
        Dictionaries that represent instances.
    '''
    with open('instances.txt') as file:
        return json.load(file)