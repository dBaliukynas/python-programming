from app.euroleague_classes.player import Player

class Team:
    '''
    A class that represents EuroLeague's team.
    Methods
    -------
    find_furthest_number_player()
        Find a player in team whose number is furthest
        from adjacent player numbers.
    '''

    def __init__(self, name, wins, losses, leaderboard_position=None):
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
        self.losses = losses
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
        team.image_source = team_dict['image_source']

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

