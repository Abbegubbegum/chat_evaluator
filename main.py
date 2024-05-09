import typer
from tinydb import TinyDB, Query, where
from tinydb.table import Document
from rich import print
import os
from os import path, listdir
import json
from typing import Dict

from DBTypes import Game, GameType, Message, Model

app = typer.Typer()
db = TinyDB('db.json')
game_types = db.table('game_types')
games = db.table('games')
models = db.table('models')
messages = db.table('messages')
tests = db.table('tests')
test_results = db.table('test_results')



@app.command()
def load_chatlogs():
    print("Loading chatlogs")
    logfiles = get_logfiles()
    for logfile in logfiles:
        load_logfile(logfile)
        new_path = path.join(path.abspath("chatlogs/loaded"), path.basename(logfile))
        os.rename(logfile, new_path)
        
    print("Chatlogs loaded") 
    


def get_logfiles() -> list[str]:
    logfiles = []

    for file in listdir("chatlogs"):
         absolute_path = path.join(path.abspath("chatlogs"), file)
         if path.isfile(absolute_path) and file.endswith(".json"):
             logfiles.append(absolute_path)
    return logfiles

def load_logfile(logfile: str):
    print(f"Loading {path.basename(logfile)} into database")
    with open(logfile, "r") as f:
      data = json.load(f)
      game_name = path.basename(f.name).split(".")[0]
      game_type_docs = game_types.search(where('name') == game_name)
      game_type = None

      if len(game_type_docs) == 0:
        game_type = GameType(game_name)
        game_type.insert_into_table(game_types)
      else:
        game_type = GameType.from_dict(game_type_docs[0])

      for game in data:
        load_game(game_type.get_id(), game)
              

def load_game(game_type: int, game_data: Dict):
    player_to_id: Dict[str, int] = {}
    for player in game_data['players']:
        model_docs = models.search(where('name') == player['model'])
        model = None

        if len(model_docs) == 0:
            model = Model(player['model'])
            model.insert_into_table(models)
        else:
            model = Model.from_dict(model_docs[0])

        player_to_id[player['name']] = model.get_id()
    
    players = [player_to_id[player['name']] for player in game_data['players']]
    game = Game(game_type, players)
    game.insert_into_table(games)

    for message in game_data['messages']:
        sender = player_to_id[message['sender']]

        message = Message(sender, game.get_id(), message['content'], message['turn'])
        message.insert_into_table(messages)



         
	

if __name__ == "__main__":
	app()