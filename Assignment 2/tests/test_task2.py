import unittest
import copy
from data import testdata
from task2 import task2

class TestSeason(unittest.TestCase):
    def test_find_best_players_by_value_one_player(self):
        result = testdata.season1.find_best_players_by_value('points')[0]
        self.assertEqual(result,
        testdata.season1.teams['Zalgiris Kaunas'].players['Niels Giffey'])

    def test_find_best_players_by_value_list_length(self):
        result = len(testdata.season1.find_best_players_by_value('points'))
        self.assertEqual(result, 1)

    def test_find_best_players_by_value_multiple_players(self):
        result = (testdata.season2.find_best_players_by_value('points')[0].points
                  == testdata.season2.find_best_players_by_value('points')[1].points)
        self.assertTrue(result)

    def test_find_best_players_by_value_wrong_attribute(self):
        self.assertRaises(AttributeError, lambda:
                          testdata.season1.find_best_players_by_value('nationality'))



    def test_find_highest_streak_teams_one_team(self):
        result = testdata.season2.find_highest_streak_teams('win_streak')[0]
        self.assertEqual(result, testdata.season2.teams['FC Bayern Munich'])

    def test_find_highest_streak_teams_list_length(self):
        result = len(testdata.season2.find_highest_streak_teams('win_streak'))
        self.assertEqual(result, 1)

    def test_find_highest_streak_teams_multiple_teams(self):
        result = (testdata.season1.find_highest_streak_teams('win_streak')[0].win_streak
        == testdata.season1.find_highest_streak_teams('win_streak')[1].win_streak)
        self.assertTrue(result)

    def test_find_highest_streak_teams_wrong_attribute(self):
        self.assertRaises(AttributeError, lambda:
                          testdata.season1.find_highest_streak_teams('wins'))

class TestGame(unittest.TestCase):
    def test_add_streak(self):

        team1_loss = testdata.season2.teams['FC Barcelona'].loss_streak
        team2_win = testdata.season2.teams['Anadolu Efes Istanbul'].win_streak

        self.assertEqual(team1_loss, 1)
        self.assertEqual(team2_win, 0)

        new_season2 = copy.deepcopy(testdata.season2)
        task2.Game('Anadolu Efes Istanbul vs FC Barcelona', 29,
                      task2.TeamPerformance(new_season2.teams['Anadolu Efes Istanbul'],
                                            108, 111, 44.2, 42.9,
                                            85.4, 11, 17, 13, 13, 5, 12),
                      task2.TeamPerformance(new_season2.teams['FC Barcelona'],
                                            110, 94, 53.8, 40.0,
                                            87.0, 11, 23, 20, 1, 0, 22 ))

        new_team1_loss = new_season2.teams['FC Barcelona'].loss_streak
        new_team2_win = new_season2.teams['Anadolu Efes Istanbul'].win_streak

        self.assertEqual(new_team1_loss, 2)
        self.assertEqual(new_team2_win, 1)

        task2.Game('Anadolu Efes Istanbul vs FC Barcelona', 29,
                      task2.TeamPerformance(new_season2.teams['Anadolu Efes Istanbul'],
                                            108, 80, 44.2, 42.9,
                                            85.4, 11, 17, 13, 13, 5, 12),
                      task2.TeamPerformance(new_season2.teams['FC Barcelona'],
                                            110, 94, 53.8, 40.0,
                                            87.0, 11, 23, 20, 1, 0, 22 ))

        new_team1_loss = new_season2.teams['FC Barcelona'].loss_streak
        new_team2_win = new_season2.teams['Anadolu Efes Istanbul'].win_streak

        self.assertEqual(new_team1_loss, 0)
        self.assertEqual(new_team2_win, 0)

    def test_count_performance_difference(self):
        result = list(testdata.season1.games['Zalgiris Kaunas vs FC Barcelona']
                      .count_performance_difference().values())[0]

        expected_values = [-7, 5, -6, -1.6, 0, 37, 7, 12, 2.9, -10, -9.6]
        for value, expected_value in zip(result.values(), expected_values):
            self.assertEqual(value, expected_value)

        result = list(testdata.season1.games['FC Barcelona vs AS Monaco']
                      .count_performance_difference().values())[0]
        expected_values = [-9, 3, 2, 16.4, 0, 5, 19, 6, 12.7, -1, 2.4]

        for value, expected_value in zip(result.values(), expected_values):
            self.assertEqual(value, expected_value)

    def test_find_better_team_by_value(self):
        team1 = testdata.season1.teams['Zalgiris Kaunas']
        team2 = testdata.season1.teams['FC Barcelona']
        expected_values = [team2, team1, team2, team2, None, team1, team1,
                            team1, team1, team2, team2]
        attributes = ['assists', 'blocks', 'defensive_rebounds',
                      'free_throw_percent', 'offensive_rebounds',
                      'performance_index_rating', 'points', 'steals',
                      'three_point_percent', 'turnovers', 'two_point_percent']

        for attribute, expected_value in zip(attributes, expected_values):
            result = testdata.season1.games['Zalgiris Kaunas vs FC Barcelona'] \
                .find_better_team_by_value(attribute)
            self.assertEqual(result, expected_value)

class TestTeam(unittest.TestCase):
    def test_find_furthest_number_players_one_player(self):
        result = testdata.season1.teams['Zalgiris Kaunas'] \
            .find_furthest_number_players()[0]
        self.assertEqual(result, testdata.season1.teams['Zalgiris Kaunas'] \
                         .players['Tai Webster'])

    def test_find_furthest_number_players_multiple_players(self):

        result = testdata.season2.teams['CSKA Moscow'].find_furthest_number_players()

        player1 = testdata.season2.teams['CSKA Moscow'] \
            .players['Alexander Khomenko']
        player2 = testdata.season2.teams['CSKA Moscow'] \
            .players['Janis Strelnieks']

        self.assertEqual(result, [player1, player2])




if __name__ == '__main__':
    unittest.main()