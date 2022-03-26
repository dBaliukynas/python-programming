from task2 import task2
season1 = task2.Season('2021-22')
season1.add_team(task2.Team('Zenit St Petersburg', 14, 9, 6))
season1.add_team(task2.Team('Panathinaikos OPAP Athens', 7, 19, 17))
season1.add_team(task2.Team('Zalgiris Kaunas', 7, 20, 18))
season1.add_team(task2.Team('FC Barcelona', 21, 6, 1))
season1.add_team(task2.Team('AS Monaco', 12, 13, 8))
season1.teams['Zenit St Petersburg'].add_player(task2.Player('Tyson', 'Carter', 1, 'USA', 'Guard',
                                                        1.0, 0.5, 1.2, 0.5, 0.0,
                                                        0.2))
season1.teams['Zenit St Petersburg'].add_player(task2.Player('Jordan', 'Loyd', 2, 'USA', 'Guard',
                                                        13.2, 4.0, 3.9, 1.0, 0.1,
                                                        14.4))
season1.teams['Zalgiris Kaunas'].add_player(task2.Player('Niels', 'Giffey', 3, 'Germany',
                                                    'Forward', 55.6, 4.5, 0.7, 0.5, 0.1,
                                                    4.7))
season1.teams['Zalgiris Kaunas'].add_player(task2.Player('Karolis', 'Lukosiunas', 1, 'Lithuania',
                                                    'Forward', 3.1, 0.8, 0.5, 0.3, 0.0,
                                                    0.9))
season1.teams['Zalgiris Kaunas'].add_player(task2.Player('Tai', 'Webster', 12, 'New Zealand',
                                                    'Guard', 4.6, 1.1, 1.8, 0.4, 0.1,
                                                    2.8))

game1 = task2.Game('Zalgiris Kaunas vs FC Barcelona', 29, 
              task2.TeamPerformance(season1.teams['Zalgiris Kaunas'], 108, 91, 44.2, 42.9,
                              85.4, 11, 17, 13, 13, 5, 12),
              task2.TeamPerformance(season1.teams['FC Barcelona'], 71, 84, 53.8, 40.0,
                              87.0, 11, 23, 20, 1, 0, 22 ))
game2 = task2.Game('FC Barcelona vs AS Monaco', 28, 
               task2.TeamPerformance(season1.teams['FC Barcelona'], 88, 91, 44.2, 42.9,
                              82.4, 14, 15, 9, 7, 6, 20),
               task2.TeamPerformance(season1.teams['AS Monaco'], 83, 72, 41.8, 30.2,
                              66.0, 14, 13, 18, 1, 3, 21 ))
season1.add_game(game1)
season1.add_game(game2)

season2 = task2.Season('2020-21')
season2.add_team(task2.Team('FC Barcelona', 24, 10, 1))
season2.add_team(task2.Team('Anadolu Efes Istanbul', 22 , 12, 3))
season2.add_team(task2.Team('FC Bayern Munich', 21, 13, 5))
season2.add_team(task2.Team('CSKA Moscow', 24, 10, 2))
season2.teams['FC Barcelona'].add_player(task2.Player('Leo', 'Westermann', 2, 'France', 'Guard',
                                                        1.0, 0.5, 1.2, 0.5, 0.0,
                                                        0.2))
season2.teams['CSKA Moscow'].add_player(task2.Player('Alexander', 'Khomenko', 4, 'Russian Federation', 'Guard',
                                                        2.3, 5.1, 2.7, 12.2, 1.8,
                                                        8.8))
season2.teams['CSKA Moscow'].add_player(task2.Player('Janis', 'Strelnieks', 13, 'Latvia',
                                                    'Forward', 7.2, 3.1, 4.5, 2.5, 1.6,
                                                    7.2))
season2.teams['CSKA Moscow'].add_player(task2.Player('Michael', 'Eric', 50, 'Nigeria',
                                                    'Center', 7.8, 3.8, 0.5, 0.5, 0.7,
                                                    7.3))
season2.teams['CSKA Moscow'].add_player(task2.Player('Nikola', 'Milutinov', 33, 'New Serbia',
                                                    'Center', 7.8, 5.5, 1.8, 11.2, 4.2,
                                                    8.5))

game1 = task2.Game('Anadolu Efes Istanbul vs FC Barcelona', 29, 
              task2.TeamPerformance(season2.teams['Anadolu Efes Istanbul'], 108, 91, 44.2, 42.9,
                              85.4, 11, 17, 13, 13, 5, 12),
              task2.TeamPerformance(season2.teams['FC Barcelona'], 110, 104, 53.8, 40.0,
                              87.0, 11, 23, 20, 1, 0, 22 ))
game2 = task2.Game('FC Barcelona vs FC Bayern Munich', 28, 
               task2.TeamPerformance(season2.teams['FC Barcelona'], 88, 91, 44.2, 42.9,
                              82.4, 14, 15, 9, 7, 6, 20),
               task2.TeamPerformance(season2.teams['FC Bayern Munich'], 93, 92, 41.8, 30.2,
                              66.0, 14, 13, 18, 1, 3, 21 ))
season1.add_game(game1)
season1.add_game(game2)
