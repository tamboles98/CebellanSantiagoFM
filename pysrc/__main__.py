import json
import sys
from alternator import alternator
import data_extraction_tools as det
from request_handler import request_handler
from alternator import alternator

API_KEY = sys.argv[1]
rh = request_handler(API_KEY)

servers = ["EUW", "KR", "NA", "EUNE"]

diamond_leagues = [det.get_summoner_ids_from_league(rh.get_diamond_i(server)) for server in servers]
diamond_iterator = alternator(index = servers, iterators = diamond_leagues)
for i, b in enumerate(diamond_iterator):
    print(i)