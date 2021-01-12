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


def get_info_from_match_list(response: Response = None) -> list:
    """Extrae los datos del json de respuesta a una petición de datos de partida
    a la API de riot games (/lol/match/v4/matches/) y los pone en formato de
    lista

    Parameters
    ----------
    response : Response
        La respuesta con los datos de la partida. Si no se le pasa nada devuelve
        una lista con los nombres de los campos de la lista que devuelve cuando
        sí se le pasa una partida

    Returns
    -------
    list
        Una lista con los datos de la partida, para saber que significa cada
        entrada llamar a la función sin parametros.
    """
    if response is None:
        return (["gameId", "gameVersion", "winner"] +
                ["blueban{}".format(i) for i in range(5)] +
                ["redban{}".format(i) for i in range(5)] +
                ["bluepick{}".format(i) for i in range(5)] +
                ["redpick{}".format(i) for i in range(5)]
        )
    matchdata = response.json()
    #Hay dos equipos, rojo y azul. Dentro de la API el equipo azul viene
    # referido como 100 y el rojo como 200
    trad = {100: "blue", 200: "red"}
    dev = list()
    dev.append(matchdata["gameId"])
    dev.append(matchdata["gameVersion"])
    #Primero añade los bans
    aux = {}
    for team in matchdata["teams"]:
        teamname = trad[team["teamId"]]
        aux[teamname]= [ban["championId"] for ban in team["bans"]]
        if team["win"] == "Win":
            aux["win"] = teamname
    dev.append(aux["win"])
    dev += aux["blue"]
    dev += aux["red"]
    #Despues los picks
    dev += [participant["championId"] for
                    participant in matchdata["participants"]
                    if participant["teamId"] == 100]
    dev += [participant["championId"] for
                    participant in matchdata["participants"]
                    if participant["teamId"] == 200]
    return dev
