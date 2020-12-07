from typing import Iterable
from data_extraction_tools import get_summoner_ids_from_league
from request_handler import request_handler
from itertools import chain
import datetime

#A veces para conseguir suficientes jugadores necesitamos varias paginas.
# Este metodo hace precisamente eso y junta las paginas en un solo iterador.
def get_multiple_pages_diamond(rh: request_handler, server: str, pages: int) -> Iterable:
    return chain(*(get_summoner_ids_from_league(rh.get_diamond_i(
        server=server, params= {"page": i}))
        for i in range(1, pages + 1)))


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0
