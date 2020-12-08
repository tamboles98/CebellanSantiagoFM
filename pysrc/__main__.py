import json
import sys
from alternator import alternator
import data_extraction_tools as det
from request_handler import request_handler
from utilities import get_multiple_pages_diamond, unix_time_millis, check_progress, save_progress
import datetime

#Definimos la configuración ---------

API_KEY = sys.argv[1] #La api key se pasa como argumento
servers = ["EUW", "KR", "NA", "EUNE"] #Los servidores que vamos a utilizar.
#corea (KR) esta muy lejos por lo que a veces da error 504.
desired_matches = 30000 #Los datos de cuantas partidas queremos obtener.
players_til_dump = 100 #Cuantos jugadores analizar antes de guardar el progreso
save_progress_path = "data/pickle_progress" #Donde se guardara el progreso
#Fecha a partir de la cual queremos partidas
startime = int(unix_time_millis(datetime.datetime(2020, 12, 3)))

#Inicializamos valores ------------

rh = request_handler(API_KEY) #La api key queda almacenada en el objeto que
# se encarga de las requests


#Estos son dos sets que llevan cuenta del progreso de la ejecución. Los iremos
# guardando en memoria para asi no tener que empezar de 0 cada vez que guardamos
analized_players, analized_matches = check_progress(save_progress_path)
desired_matches = desired_matches - len(analized_matches)
if desired_matches <= 0:
    sys.exit("Datos ya existentes")

matches = list()

diamond_leagues = [get_multiple_pages_diamond(rh, server, 4)for server in servers]
diamond_iterator = alternator(index = servers, iterators = diamond_leagues)

tildump = 0
for server, summoner in diamond_iterator:
    if (server, summoner) in analized_players:
        continue
    try:
        account = det.get_summoner_account_id(rh.get_account_id(server, summoner))
        history = det.get_summoner_history(rh.get_match_history(server,
            account, params = {"queue": 420, "beginTime": startime}))
    except (ValueError, RuntimeError):
        continue #Si salta este buscando el historial eso quiere decir que el
        # usuario no jugo ninguna partida en el perido para el que hemos pedido
        # el historial. Tambien puede significar que el servidor no ha respondido
        # a la request por cualquier motivo.
    for match in history:
        if (server, match) not in analized_matches:
            try:
                matches.append(det.get_info_from_match(rh.get_match(server, match)))
            except ValueError: #Puede saltar una request con respuesta 504
                continue
            analized_matches.add((server, match))
    
    analized_players.add((server, summoner))
    #Comprueba si tiene que guardar el progreso.
    tildump += 1
    if tildump >= players_til_dump:
        save_progress(save_progress_path, analized_players, analized_matches)
        with open("data/matches.json", mode = "w") as file:
            json.dump(matches, file)

    if len(analized_matches) >= desired_matches:
        break # Salir del bucle si ya obtuvimos suficientes partidas.

    
    
with open("data/matches.json", mode = "w") as file:
    json.dump(matches, file)