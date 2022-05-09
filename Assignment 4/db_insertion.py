from app.euroleague_classes.season import Season
from app.euroleague_classes.team import Team
from app.euroleague_classes.player import Player
from app.instance_utils import file_operations as fo
from app.models.player import PlayerModel
from app.db import db
from app import create_app


season = fo.convert_to_instances(fo.load_from_file(
    'app/static/data/season.json'), vars())

for team in season[0].teams.values():
    for player in team.players.values():
        player = PlayerModel(player.name, player.surname, player.number, player.nationality, player.position, player.points,
                             player.rebounds, player.assists, player.steals, player.blocks, player.performance_index_rating,
                             player.image_source)

        with create_app().app_context():
            db.session.add(player)
            db.session.commit()

with create_app().app_context():
    query = PlayerModel.query.all()            
    print(f'{query}\n')
    print(f'Inserted {len(query)} rows.')
