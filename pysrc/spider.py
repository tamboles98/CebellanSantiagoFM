from data_extraction_tools import (get_summoner_ids_from_league,
                                    get_summoner_account_id,
                                    get_summoner_history)
from request_handler import request_handler
from typing import Iterable
from itertools import chain
from alternator import alternator
import datetime
from utilities import unix_time_millis, read_format_save_csv
import re
import sys
import csv

#A veces para conseguir suficientes jugadores necesitamos varias paginas.
# Este metodo hace precisamente eso y junta las paginas en un solo iterador.
def get_multiple_pages_diamond(rh: request_handler, server: str, pages: int = 3) -> Iterable:
    return chain(*(get_summoner_ids_from_league(rh.get_diamond_i(
        server=server, params= {"page": i}))
        for i in range(1, pages + 1)))


def get_account(summoner: str, rh: request_handler, server: str) -> str:
    summoner_info = rh.get_account_id(server= server, summoner_id= summoner)
    return get_summoner_account_id(summoner_info)


def get_history(account: str, rh: request_handler, server: str,
                startdate: float = None) -> list:
    params = {"queue": 420}
    if startdate is not None:
        params["beginTime"] = startdate

    try:
        history_data = rh.get_match_history(server, account, params)
    except ValueError as error:
        if re.match("^404", str(error)):
            raise ValueError("expected 404")
        else:
            raise error
    return get_summoner_history(history_data)


def player_pipeline(summoner: str, rh: request_handler, server: str, startdate) -> list:
    account = get_account(summoner, rh, server)
    return get_history(account, rh, server, startdate)


def spider(rh: request_handler, servers: list, ngames: int, npages: int = 10,
            startdate: datetime.datetime = None) -> dict:

    #Busca archivos locales con partidas y jugadores como manera de controlar
    # el progreso. Esto es util en caso de que previamente haya habido un error
    # durante la ejecución para no tener que empezar desde el principio.
    players_analysed = read_format_save_csv("data/spider/analysed_players.csv",
                                            keys = servers)
    match_ids = read_format_save_csv("data/spider/matches_to_analyse.csv",
                                    keys= servers)
    
    if sum(len(matches) for matches in match_ids.values()) >= ngames:
        print("Se encontraron suficientes ({}) partidas en archivos locales".format(
            sum(len(matches) for matches in match_ids.values())
        ))
        return match_ids

    if startdate is None:#Si no se le introduce fecha cogera la fecha de hoy
        startdate = datetime.datetime.today() - datetime.timedelta(days = 7)
    unix_startdate = int(unix_time_millis(startdate))

    #Saca listas con jugadores a analizar para cada región
    players_by_regions =  {server: get_multiple_pages_diamond(rh, server, npages)
                for server in servers}

    player_iterator = alternator(players_by_regions)
    with open('data/spider/matches_to_analyse.csv', 'a') as matchesfile, open("data/spider/analysed_players.csv", "a") as playersfile:
        matches_writer = csv.writer(matchesfile, delimiter = ",", quotechar = "\"")
        players_writer = csv.writer(playersfile, delimiter = ",", quotechar = "\"")
        for server, player in player_iterator:
            if player in players_analysed[server]:
                continue

            try:
                newgames = set(player_pipeline(player, rh, server, unix_startdate))
            except ValueError as error:
                if str(error) == "expected 404":
                    print("hello")
                    continue
                else:
                    raise error
            
            newgames = newgames - match_ids[server]
            match_ids[server] = match_ids[server].union(newgames)

            for match in newgames:
                matches_writer.writerow([server, match])
            players_writer.writerow([server, player])
            if sum(len(matches) for matches in match_ids.values()) >= ngames:
                break
    
    print("spider completado: se han obtenido {} partidas".format(
            sum(len(matches) for matches in match_ids.values())))
    return match_ids


api_key = sys.argv[1]
request_hadler = request_handler(api_key)
servers = ["EUW", "KR", "NA", "EUNE"]
spider(request_hadler, servers, 30000)

