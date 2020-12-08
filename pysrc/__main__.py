import json
import sys
from alternator import alternator
import data_extraction_tools as det
from request_handler import request_handler
from utilities import get_multiple_pages_diamond, unix_time_millis
import datetime

API_KEY = sys.argv[1] #La api key se pasa como argumento
rh = request_handler(API_KEY) #La api key queda almacenada en el objeto que
# se encarga de las requests

servers = ["EUW", "KR", "NA", "EUNE"] #Los servidores que vamos a utilizar.
#corea (KR) esta muy lejos por lo que a veces da error 504.

desired_matches = 30000 #Los datos de cuantas partidas queremos obtener.

diamond_leagues = [get_multiple_pages_diamond(rh, server, 4)for server in servers]
diamond_iterator = alternator(index = servers, iterators = diamond_leagues)

analiced_matches = set() #En este conjunto iran las partidas que ya hemos
# analizado, asi evitaremos
matches = list()

#Solo cogera partidas del parche 10.22
startime = int(unix_time_millis(datetime.datetime(2020, 12, 3)))
#La API no deja pedir el historial de más de una semana. Con partidas de una
# semana debería ser suficiente para obtener un tamaño de muestra aceptable
#endtime = startime + 3600*24*7*1000 -10
matches = []
for server, summoner in diamond_iterator:
    account = det.get_summoner_account_id(rh.get_account_id(server, summoner))
    try:
        history = det.get_summoner_history(rh.get_match_history(server,
            account, params = {"queue": 420, "beginTime": startime}))
    except RuntimeError:
        continue #Si salta este buscando el historial eso quiere decir que el
        # usuario no jugo ninguna partida en el perido para el que hemos pedido
        # el historial.
    for match in history:
        if tuple(server, match) not in analiced_matches:
            try:
                matches.append(det.get_info_from_match(rh.get_match(server, match)))
            except ValueError: #Puede saltar una request con respuesta 504
                continue
            analiced_matches.add(tuple(server, match))
    if len(analiced_matches) >= desired_matches:
        break # Salir del bucle si ya obtuvimos suficientes partidas.
    

with open("data/matches.json", mode = "w") as file:
    json.dump(matches, file)