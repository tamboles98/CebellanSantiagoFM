import json
import sys
import data_extraction_tools as det
from request_handler import request_handler

API_KEY = sys.argv[1]
rh = request_handler(API_KEY)

servers = ["EUW", "KR", "NA", "EUNE"]

d1 = det.get_summoner_ids_from_league(rh.get_diamond_i("EUW"))
a = next(d1)
d1.get


