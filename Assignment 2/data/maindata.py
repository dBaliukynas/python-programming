from task2 import task2

season1 = task2.Season('2021-22')
season1.add_team(task2.Team('Zenit St Petersburg', 14, 9, 6))
season1.add_team(task2.Team('Panathinaikos OPAP Athens', 7, 19, 17))
season1.add_team(task2.Team('Zalgiris Kaunas', 7, 20, 18))
season1.add_team(task2.Team('FC Barcelona', 21, 6, 1))
season1.teams['Zenit St Petersburg'].add_player(task2.Player('Tyson', 'Carter', 1, 'USA', 'Guard',
                                                        1.0, 0.5, 1.2, 0.5, 0.0,
                                                        0.2))
season1.teams['Zenit St Petersburg'].add_player(task2.Player('Jordan', 'Loyd', 2, 'USA', 'Guard',
                                                        13.2, 4.0, 3.9, 1.0, 0.1,
                                                        14.4))
season1.teams['Zalgiris Kaunas'].add_player(task2.Player('Niels', 'Giffey', 100, 'Germany',
                                                    'Forward', 5.6, 2.6, 0.7, 0.5, 0.1,
                                                    4.7))
season1.teams['Zalgiris Kaunas'].add_player(task2.Player('Karolis', 'Lukosiunas', 50, 'Lithuania',
                                                    'Forward', 3.1, 0.8, 0.5, 0.3, 0.0,
                                                    0.9))
season1.teams['Zalgiris Kaunas'].add_player(task2.Player('Tai', 'Webster', 70, 'New Zealand',
                                                    'Guard', 4.6, 1.1, 1.8, 0.4, 0.1,
                                                    2.8))
season1.teams['Zalgiris Kaunas'].add_player(task2.Player('Paulius', 'Jankunas', 77, 'Lithuania',
                                                    'Guard', 4.6, 1.1, 1.8, 0.4, 0.1,
                                                    2.8))


game1 = task2.Game('Zalgiris Kaunas vs FC Barcelona', 29,
              task2.TeamPerformance(season1.teams['Zalgiris Kaunas'], 108, 91, 44.2, 42.9,
                              85.4, 11, 17, 13, 13, 5, 12),
              task2.TeamPerformance(season1.teams['FC Barcelona'], 71, 84, 53.8, 40.0,
                              87.0, 11, 23, 20, 1, 0, 22 ))
game2 = task2.Game('Zalgiris Kaunass vs FC Barcelona', 29,
              task2.TeamPerformance(season1.teams['FC Barcelona'], 108, 91, 44.2, 42.9,
                              85.4, 11, 17, 13, 13, 5, 12),
              task2.TeamPerformance(season1.teams['Zenit St Petersburg'], 71, 84, 53.8, 40.0,
                              87.0, 11, 23, 20, 1, 0, 22 ))
season1.add_game(game1)
season1.add_game(game2)

