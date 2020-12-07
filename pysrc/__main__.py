import json
import sys
from alternator import alternator
import data_extraction_tools as det
from request_handler import request_handler
from utilities import get_multiple_pages_diamond, unix_time_millis
import datetime

API_KEY = sys.argv[1]
rh = request_handler(API_KEY)

servers = ["EUW", "KR", "NA", "EUNE"]

diamond_leagues = [get_multiple_pages_diamond(rh, server, 3)for server in servers]
diamond_iterator = alternator(index = servers, iterators = diamond_leagues)

analiced_matches = set()

#Solo cogera partidas del parche 10.22
startime = int(unix_time_millis(datetime.datetime(2020, 12, 3)))
#La API no deja pedir el historial de más de una semana. Con partidas de una
# semana debería ser suficiente para obtener un tamaño de muestra aceptable
#endtime = startime + 3600*24*7*1000 -10
i = 0
for  server, summoner in diamond_iterator:
    account = det.get_summoner_account_id(rh.get_account_id(server, summoner))
    try:
        history = det.get_summoner_history(rh.get_match_history(server,
            account, params = {"queue": 420, "beginTime": startime}))
    except RuntimeError:
        continue
    if i >= 20:
        break
    i += 1

print(i)