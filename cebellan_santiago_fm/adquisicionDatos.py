import requests
import time
from itertools import chain


class request_handler():
    # Lista con los distintos servidores contra los que vamos lanzar queries.
    # Mi API keys no me permite lanzar más de 100 queries cada 2 minutos AL MISMO
    # servidor, por eso usare varios.
    ROUTES = {"EUW": "euw1.api.riotgames.com", #Europe West
                "KR": "kr.api.riotgames.com", #Korea
                "NA": "na1.api.riotgames.com", #North America
                "EUNE": "eun1.api.riotgames.com"} #Europe Nordic & East
    LIMITSHORT = (20, 1)
    LIMITLONG = (100, 120)
    
    def __init__(self, api_key):
        ti = time.time()
        self.short = {"EUW": (0, ti), "KR": (0, ti),
                        "NA": (0, ti), "EUNE": (0, ti)}
        self.long = {"EUW": (0, ti), "KR": (0, ti),
                        "NA": (0, ti), "EUNE": (0, ti)}
        self.api_key = api_key


    def get_diamond_i(self, server):
        url = request_handler.prepare_url(server = request_handler.ROUTES[server],
            endpoint="/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=1")
        headers = {
            'X-Riot-Token': self.api_key
            }

        return self.safe_request(server=server, url=url, headers=headers)


    def get_account_id(self, server, summoner_id):
        endpoint = "/lol/summoner/v4/summoners/{}".format(summoner_id)
        url = request_handler.prepare_url(server = request_handler.ROUTES[server],
            endpoint= endpoint)
        headers = {
            'X-Riot-Token': self.api_key
            }
        
        return self.safe_request(server=server, url=url, headers=headers)

    
    def get_match_history(self, server, account_id):
        endpoint = "/lol/match/v4/matchlists/by-account/{}".format(account_id)
        url = request_handler.prepare_url(server = request_handler.ROUTES[server],
            endpoint= endpoint)
        headers = {
            'X-Riot-Token': self.api_key
            }
        
        return self.safe_request(server=server, url=url, headers=headers)
    
    def get_match(self, server, match_id):
        endpoint = "/lol/match/v4/matches/{}".format(match_id)
        url = request_handler.prepare_url(server = request_handler.ROUTES[server],
            endpoint= endpoint)
        headers = {
            'X-Riot-Token': self.api_key
            }
        
        return self.safe_request(server=server, url=url, headers=headers)


    @staticmethod
    def prepare_url(server, endpoint):
        return "https://" + server + endpoint

    #A partir los metodos sirven para asegurarse que no se hacen demasiadas
    # requests a ningún server.

    def safe_request(self, server, url, headers):
        if self.ready_for_request(server):
            self.short[server][0] += 1
            self.long[server][0] += 1
            return requests.request("GET", url, headers=headers)
        #Si hemos alcanzado algún limite comprueba que no sea hora de
        # resetear los tiempos
        if self.check_timers_reset(server) and self.ready_for_request(server):
            self.short_n[server] += 1
            self.long_n[server] += 1
            return requests.request("GET", url, headers=headers)
    
    #Este metodo comprueba si ya ha pasado tiempo suficiente desde el ultimo
    # reset para el server y resetea si ese es el caso.
    def check_timers_reset(self, server):
        ti = time.time() #Current time
        change = False #Comprueba si ha habido algún cambio al ejecutar esta
                        # acción
        if ti - self.short[server][1] > request_handler.LIMITSHORT[1]:
            self.short[server] = (0, ti)
            change = True
        if ti - self.long[server][1] > request_handler.LIMITLONG[1]:
            self.long[server] = (0, ti)
            change = True
        return change

    #Sleeps hasta que sea hora de resetear
    def wait_for_reset(self):
        ti = time.time()
        waitime = (request_handler.LIMITLONG[1] -
            min(ti - i[1] for i in self.long.values()))
        time.sleep(waitime)
        time.sleep(1)
        ti = time.time()
        self.short = {"EUW": (0, ti), "KR": (0, ti),
                        "NA": (0, ti), "EUNE": (0, ti)}
        self.long = {"EUW": (0, ti), "KR": (0, ti),
                        "NA": (0, ti), "EUNE": (0, ti)}
        return None

    def ready_for_request(self, server):
        return (self.short[server][0] < request_handler.LIMITSHORT[0] and
        self.long[server][0] < request_handler.LIMITLONG[0])


        