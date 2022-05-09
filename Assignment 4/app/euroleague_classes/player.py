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
                     
        player.image_source = player_dict['image_source']

        player.fullname = player.name + ' ' + player.surname

        return player
