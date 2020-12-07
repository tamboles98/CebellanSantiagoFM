import requests
import time

#IMPORTANTE: Para que request_handler no ralentice mucho el programa es muy
# importante hacer las llamadas a los distintos sevidores de forma alterna.
# Nunca hacer todas las llamadas al mismo servidor de forma seguida.
class request_handler():
    # Lista con los distintos servidores contra los que vamos lanzar queries.
    # Mi API keys no me permite lanzar más de 100 queries cada 2 minutos AL MISMO
    # servidor, por eso usare varios.
    ROUTES = {"EUW": "euw1.api.riotgames.com", #Europe West
                "KR": "kr.api.riotgames.com", #Korea
                "NA": "na1.api.riotgames.com", #North America
                "EUNE": "eun1.api.riotgames.com"} #Europe Nordic & East
    LIMITSHORT = 1
    LIMITLONG = 120
    
    def __init__(self, api_key):
        self.api_key = api_key


    def get_diamond_i(self, server, params = {}):
        url = request_handler.prepare_url(server = request_handler.ROUTES[server],
            endpoint="/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I")
        headers = {
            'X-Riot-Token': self.api_key
            }

        return self.safe_request(url=url, headers=headers, params=params)


    def get_account_id(self, server, summoner_id, params={}):
        endpoint = "/lol/summoner/v4/summoners/{}".format(summoner_id)
        url = request_handler.prepare_url(server = request_handler.ROUTES[server],
            endpoint= endpoint)
        headers = {
            'X-Riot-Token': self.api_key
            }
        
        return self.safe_request(url=url, headers=headers, params=params)

    
    def get_match_history(self, server, account_id, params = {}):
        endpoint = "/lol/match/v4/matchlists/by-account/{}".format(account_id)
        url = request_handler.prepare_url(server = request_handler.ROUTES[server],
            endpoint= endpoint)
        headers = {
            'X-Riot-Token': self.api_key
            }
        
        return self.safe_request(url=url, headers=headers,
                params = params)
    
    def get_match(self, server, match_id):
        endpoint = "/lol/match/v4/matches/{}".format(match_id)
        url = request_handler.prepare_url(server = request_handler.ROUTES[server],
            endpoint= endpoint)
        headers = {
            'X-Riot-Token': self.api_key
            }
        
        return self.safe_request(url=url, headers=headers)


    @staticmethod
    def prepare_url(server, endpoint):
        return "https://" + server + endpoint

    #A partir los metodos sirven para asegurarse que no se hacen demasiadas
    # requests a ningún server.
    def safe_request(self, url, headers, params = {}):
        #Intenta hacer la request, cuando has hecho demasiadas request el
        # el servidor devuelve None.
        dev = requests.request("GET", url, headers=headers, params = params)
        #Si el servidor delvuelve None esperara antes de volver a intentar hacer
        # la request.
        if dev.status_code == 429:
            time.sleep(self.LIMITSHORT)
            dev = requests.request("GET", url, headers=headers, params = params)
        if dev.status_code == 429:
            time.sleep(self.LIMITLONG - self.LIMITSHORT)
            dev = requests.request("GET", url, headers=headers, params = params)
        #Una vez ya ha hecho todos los intentos esperados comprueba que la
        # request ha tenido el resultado esperado
        if dev is None:
            raise RuntimeError("got not response from server when it should")
        elif dev.status_code == 404:
            raise RuntimeError("request status 404. tried to get unexistent data. "
                                "probably requested match history for a player"
                                "that did not play any games.")
        elif dev.status_code != 200:
            raise ValueError("bad request in: " + dev.url + " status: " +
                        str(dev.status_code))
        #Devuelve
        return dev