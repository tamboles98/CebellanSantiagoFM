import requests
import sys

#Primero el programa necesitara una key para poder acceder a la API
if len(sys.argv) <= 1:
    raise TypeError('No se ha introducido key para usar con la API')
key = sys.argv[1]

r = requests.get('https://euw1.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5', params = {'api_key' : key})

names = []
for summoner in r.json()["entries"]:
    names.append(summoner["summonerName"])