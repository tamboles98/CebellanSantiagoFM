from request_handler import request_handler
from data_extraction_tools import get_info_from_match_list
from utilities import read_format_save_csv
from alternator import alternator
import csv
import re
import sys

def scrapper(rh: request_handler,
            matchcodes_path: str = "data/spider/matches_to_analyse.csv"):
    matchcodes = read_format_save_csv(matchcodes_path)
    analysed_matches = read_format_save_csv("data/scrapper/matches.csv",
                                    keys = matchcodes.keys())
    match_iterator = alternator(matchcodes)
    nmatches = 0
    with open("data/scrapper/matches.csv", 'a') as savefile:
        matches_writer = csv.writer(savefile, delimiter = ",", quotechar = "\"")
        matches_writer.writerow(["server"] + get_info_from_match_list())
        for server, match in match_iterator:
            if match in analysed_matches[server]:
                continue
            try:
                matchdata = rh.get_match(server, match)
            except ValueError as error:
                if re.match(r"504$", str(error)):
                    continue
            matches_writer.writerow([server] + get_info_from_match_list(matchdata))
            nmatches += 1
    print("scrapper completado: se han obtenido datos de {} partidas".format(nmatches))
