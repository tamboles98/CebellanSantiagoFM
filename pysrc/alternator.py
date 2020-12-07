from itertools import cycle


class alternator():

    def __init__(self, index, iterators):
        if len(index) != len(iterators):
            raise ValueError("index and iterators have different length")
        self.__iterators = [tupl for tupl in zip(index, iterators)]
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
                print(self.exhausted)
                if not self.__iterators:
                    self.__fully_exhausted = True
                    raise StopIteration

    def __str__(self):
        return ("using iterators: {using},"
            "exhausted iterators: {exhausted}").format(
                using = str(self.__iterators),
                exhausted = str(self.exhausted)
                )
