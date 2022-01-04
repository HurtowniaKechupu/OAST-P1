#todo spolszczyć
class Configuration:
    def __init__(self, lowerValueOfArrivals, upperValueOfArrivals, seed, switching, numOfSimulations, simulationDuration, econ, ecoff, d, task):
        self.lowerValueOfArrivals = lowerValueOfArrivals    # min. średnia intensywność napływu lambda
        self.upperValueOfArrivals = upperValueOfArrivals    # max. średnia intensywność napływu lambda
        self.seed = seed                                    # ziarno dla generatora
        self.switching = switching                          # tryb z wyłączeniami: False - bez wyłączeń; True - z wyłączeniami
        self.numOfSimulations = numOfSimulations            # całkowita liczba symulacji
        self.simulationDuration = simulationDuration        # całkowity czas symulacji
        self.econ = econ                                    # czas działania serwera między przerwami
        self.ecoff = ecoff                                  # czas przerwy w działaniu serwera
        self.d = d                                          # średni czas obsługi wiadomości w serwerze
        self.task = task                                    # numer zadania do wykonania: {1, 2}

        self.numberOfMessages = 10                          # minimalna ilość zdarzeń w symulacji (ZMIENNA POMOCNICZA)
        self.lambda1 = 0.0                                  # wartość lambda dla generatora zdarzeń (ZMIENNA POMOCNICZA)
        self.warmUpTime = 10                                # rozbieg
