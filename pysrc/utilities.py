from typing import Iterable
from data_extraction_tools import get_summoner_ids_from_league
from request_handler import request_handler
from itertools import chain
import datetime
import pickle

#A veces para conseguir suficientes jugadores necesitamos varias paginas.
# Este metodo hace precisamente eso y junta las paginas en un solo iterador.
def get_multiple_pages_diamond(rh: request_handler, server: str, pages: int) -> Iterable:
    return chain(*(get_summoner_ids_from_league(rh.get_diamond_i(
        server=server, params= {"page": i}))
        for i in range(1, pages + 1)))


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


def check_progress(dirpath: str):
    try:
        with open(dirpath + "/players.pickle", "rb") as file:
            players = pickle.load(file)
    except FileNotFoundError:
        players = set()

    try:
        with open(dirpath + "/games.pickle", "rb") as file:
           games = pickle.load(file)
    except FileNotFoundError:
        games = set()
    
    return (players, games)


def save_progress(dirpath: str, players: set, games: set):
    print("saving progress...")
    with open(dirpath + "/players.pickle", "wb") as file:
        pickle.dump(players, file)
    with open(dirpath + "/games.pickle", "wb") as file:
        pickle.dump(games, file)
