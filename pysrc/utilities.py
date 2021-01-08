import datetime
import pickle
import csv


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


def check_progress(dirpath: str):
    try:
        with open(dirpath + "/players.pickle", "rb") as file:
            players = pickle.load(file)
    except FileNotFoundError:
        players = set()

    try:
        with open(dirpath + "/games.pickle", "rb") as file:
           games = pickle.load(file)
    except FileNotFoundError:
        games = set()
    
    return (players, games)


def save_progress(dirpath: str, players: set, games: set):
    print("saving progress...")
    with open(dirpath + "/players.pickle", "wb") as file:
        pickle.dump(players, file)
    with open(dirpath + "/games.pickle", "wb") as file:
        pickle.dump(games, file)


def read_format_save_csv(path: str, not_found: str = "proceed", keys: list = []) -> dict:
    """Lee el formato de archivo en el que el spider guarda su progreso y extrae
    los datos en un diccionario de conjuntos {region: set}

    Parameters
    ----------
    path : str
        El path al archivo en cuestión
    not_found : str
        Que hacer si no encuentra el archivo, dos opciones: "proceed" devuelve
        el diccionario con listas vacias y "raise" para devolver el error.
        Defaults to "proceed"

    Returns
    -------
    dict
        Diccionario de formato {region: set} con los datos del fichero.

    Raises
    ------
    """
    data = {key: set() for key in keys}
    try:
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter = ",", quotechar = "\"")
            for line in reader:
                if line[0] not in data:
                    data[line[0]] = {line[1]}
                else:
                    data[line[0]].add(line[1])
    except FileNotFoundError as error:
        if not_found == "raise":
            raise error
    return data
