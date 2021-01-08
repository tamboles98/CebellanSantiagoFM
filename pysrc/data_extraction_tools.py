from requests.models import Response

#Esto no devuelve una lista devuelve un generador
def get_summoner_ids_from_league(response: Response):
    return (player["summonerId"] for player in response.json())


def get_summoner_account_id(response: Response):
    return response.json()["accountId"]


#Esto no devuelve una lista devuelve un generador
def get_summoner_history(response: Response):
    return [match["gameId"] for match in response.json()["matches"]]


def get_info_from_match(response: Response):
    matchdata = response.json()
    #Hay dos equipos, rojo y azul. Dentro de la API el equipo azul viene
    # referido como 100 y el rojo como 200
    trad = {100: "blue", 200: "red"}
    dev = {}
    dev["gameId"] = matchdata["gameId"]
    dev["gameVersion"] = matchdata["gameVersion"]

    for team in matchdata["teams"]:
        teamname = trad[team["teamId"]]
        dev[teamname]= {"bans": [ban["championId"] for ban in team["bans"]],
                        "picks": []} #Prepara ya donde se añadiran los picks
        if team["win"] == "Win":
            dev["win"] = teamname

    #Añade los picks
    for participant in matchdata["participants"]:
        teamname = trad[participant["teamId"]]
        dev[teamname]["picks"].append(participant["championId"])

    return dev

 
