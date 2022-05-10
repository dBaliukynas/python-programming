from app.euroleague_classes.season import Season
from app.euroleague_classes.team import Team
from app.euroleague_classes.player import Player
from app.instance_utils import file_operations as fo

from app.models.player import PlayerModel
from app.models.team import TeamModel
from app.models.season import SeasonModel

from app.db import db
from app import create_app


season = fo.convert_to_instances(fo.load_from_file(
    'app/static/data/season.json'), vars())

season_instance = SeasonModel(season[0].name)
with create_app().app_context():
    db.session.add(season_instance)
    db.session.commit()

for team in season[0].teams.values():
    team_instance = TeamModel(team.name, team.wins, team.losses,
                              team.win_streak, team.loss_streak, team.leaderboard_position,  team.image_source)
    with create_app().app_context():
        db.session.add(team_instance)
        db.session.commit()

    for player in team.players.values():
        player_instance = PlayerModel(player.name, player.surname, player.number, player.nationality, player.position, player.points,
                                      player.rebounds, player.assists, player.steals, player.blocks, player.performance_index_rating,
                                      player.image_source)

        with create_app().app_context():
            db.session.add(player_instance)
            db.session.commit()

with create_app().app_context():
    query = PlayerModel.query.all()
    print(f'{query}\n')
    print(f'Player table consists of {len(query)} rows.')
