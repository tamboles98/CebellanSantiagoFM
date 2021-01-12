from itertools import cycle


class alternator():
    """Un iterador que va alternando entre varios iteradores hasta que todos se
    agotan
    """
    def __init__(self, iterators: dict):
        """Crea un objeto alternator

        Parameters
        ----------
        iterators : dict
            Un diccionario con claves el nombre con el que se referira a un
            iterador y valor el iterador|iterable en cuestión.

        """
        keys = iterators.keys()
        iters = (iter(i) for i in iterators.values())
        self.__iterators = list(zip(keys, iters))
        #Iteradores y sus indices
        self.__pos = 0 # De que iterador debe extraer a continuación
        self.__fully_exhausted = False # Si se han agotado todos los iteradores
        self.exhausted = [] # Que iteradores se han agotado


    def __iter__(self):
        return self

    def __next__(self):
        if self.__fully_exhausted:
            raise StopIteration
        dev = None
        #Intenta usar el iterador que toca. Si ese iterador esta agotado,
        # lo elimina de la lista de iteradores y vuelve a intentarlo
        while dev is None:
            pos = self.__pos % len(self.__iterators)
            try:
                dev = (self.__iterators[pos][0],
                        next(self.__iterators[pos][1]))
                self.__pos = (self.__pos + 1) % len(self.__iterators)
                return dev
            except StopIteration:
                self.exhausted.append(self.__iterators.pop(pos))
                if not self.__iterators:
                    self.__fully_exhausted = True
                    raise StopIteration

    def __str__(self):
        return ("using iterators: {using},"
            "exhausted iterators: {exhausted}").format(
                using = str(self.__iterators),
                exhausted = str(self.exhausted)
                )
