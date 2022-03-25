import unittest
import testdata

print(testdata.season1.games['Zalgiris Kaunas vs FC Barcelona'].count_performance_difference())
# print(testdata.season1.games['Zalgiris Kaunas vs FC Barcelona'].find_better_team_by_value('points'))
class TestSeason(unittest.TestCase):
    def test_find_best_player_by_value_one_player(self):
        result = testdata.season1.find_best_player_by_value('points')[0]
        self.assertEqual(result, 
        testdata.season1.teams['Zalgiris Kaunas'].players['Niels Giffey'])
        
    def test_find_best_player_by_value_list_length(self):
        result = len(testdata.season1.find_best_player_by_value('points'))
        self.assertEqual(result, 1)
        
    def test_find_best_player_by_value_multiple_players(self):
        result = (testdata.season2.find_best_player_by_value('points')[0].points 
                  == testdata.season2.find_best_player_by_value('points')[1].points)
        self.assertTrue(result)
        
    def test_find_best_player_by_value_wrong_attribute(self):
        self.assertRaises(AttributeError, lambda: 
                          testdata.season1.find_best_player_by_value('nationality'))
    
    
        
    def test_find_highest_streak_team_one_team(self):
        result = testdata.season2.find_highest_streak_team('win_streak')[0]
        self.assertEqual(result, testdata.season2.teams['FC Bayern Munich'])
        
    def test_find_highest_streak_team_list_length(self):
        result = len(testdata.season2.find_highest_streak_team('win_streak'))
        self.assertEqual(result, 1)
        
    def test_find_highest_streak_team_multiple_teams(self):
        result = (testdata.season1.find_highest_streak_team('win_streak')[0].win_streak
        == testdata.season1.find_highest_streak_team('win_streak')[1].win_streak)
        self.assertTrue(result)
        
    def test_find_highest_streak_team_wrong_attribute(self):
        self.assertRaises(AttributeError, lambda: 
                          testdata.season1.find_highest_streak_team('wins'))
            
class TestGame(unittest.TestCase):
    def test_add_streak(self):
        team1 = testdata.season1.teams['Zalgiris Kaunas'].win_streak
        team2 = testdata.season1.teams['FC Barcelona'].win_streak
        team3 = testdata.season1.teams['AS Monaco'].win_streak
        
        self.assertEqual(team1, 1)
        self.assertEqual(team2, 1)
        self.assertEqual(team3, 0)
        
    def test_count_performance_difference(self):
        pass
        
        
    
if __name__ == '__main__':
    unittest.main()