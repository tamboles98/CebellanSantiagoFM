import requests
import time


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
        self.short = time.time()
        self.long = time.time()
        self.short_n = {"EUW": 0, "KR": 0, "NA": 0, "EUNE": 0}
        self.long_n = {"EUW": 0, "KR": 0, "NA": 0, "EUNE": 0}
        self.api_key = api_key



    def get_diamond_i(self, routing):
        url = request_handler.prepare_url(routing = request_handler.ROUTES[routing],
            endpoint="/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=1")
        headers = {
            'X-Riot-Token': self.api_key
            }

        return requests.request("GET", url, headers=headers)


    def get_account_id(self, route, summoner_id):
        endpoint = "/lol/summoner/v4/summoners/{}".format(summoner_id)
        url = request_handler.prepare_url(routing = request_handler.ROUTES[route],
            endpoint= endpoint)
        headers = {
            'X-Riot-Token': self.api_key
            }
        
        return requests.request("GET", url, headers=headers)

    
    def get_match_history(self, route, account_id):
        endpoint = "/lol/match/v4/matchlists/by-account/{}".format(account_id)
        url = request_handler.prepare_url(routing = request_handler.ROUTES[route],
            endpoint= endpoint)
        headers = {
            'X-Riot-Token': self.api_key
            }
        
        return requests.request("GET", url, headers=headers)

    
    def get_match(self, route, match_id):
        endpoint = "/lol/match/v4/matches/{}".format(match_id)
        url = request_handler.prepare_url(routing = request_handler.ROUTES[route],
            endpoint= endpoint)
        headers = {
            'X-Riot-Token': self.api_key
            }
        
        return requests.request("GET", url, headers=headers)


    @staticmethod
    def prepare_url(routing, endpoint):
        return "https://" + routing + endpoint

    
    def safe_request(self, route, url, headers):
        if (self.short_n[route] < request_handler.LIMITSHORT[0] and
            self.long_n[route] < request_handler.LIMITLONG[0]):
            self.short_n[route] += 1
            self.long_n[route] += 1
            return requests.request("GET", url, headers=headers)
        #Si hemos alcanzado algún limite comprueba que no sea hora de
        # resetear los tiempos
        self.check_timers_reset()
        if (self.short_n[route] < request_handler.LIMITSHORT[0] and
            self.long_n[route] < request_handler.LIMITLONG[0]):
            self.short_n[route] += 1
            self.long_n[route] += 1
            return requests.request("GET", url, headers=headers)
    
    def check_timers_reset(self):
        if time.time() - self.short > request_handler.LIMITSHORT[1]:
            self.short_n = {"EUW": 0, "KR": 0, "NA": 0, "EUNE": 0}
            self.short = time.time()
        if time.time() - self.long > request_handler.LIMITLONG[1]:
            self.long_n = {"EUW": 0, "KR": 0, "NA": 0, "EUNE": 0}
            self.long = time.time()
        return None

    
    def check_sleep(self):
        if (all(i >= request_handler.LIMITSHORT[0] for i in self.short_n.values())
            and 
            all(i >= request_handler.LIMITLONG[0] for i in self.long_n.values())):
        
            