#todo zmienic komentarze
class Ustawienia:
    def __init__(self, minLambda, maxLambda, seed, wylaczanie, liczbaSymulacji, dlugoscSymulacji, econ, ecoff, d, zadanie):
        self.minLambda = minLambda                          # min. średnia intensywność napływu lambda
        self.maxLambda = maxLambda                          # max. średnia intensywność napływu lambda
        self.seed = seed                                    # ziarno dla generatora
        self.wylaczanie = wylaczanie                        # False - bez wyłączeń; True - z wyłączeniami
        self.liczbaSymulacji = liczbaSymulacji              # całkowita liczba symulacji
        self.dlugoscSymulacji = dlugoscSymulacji            # całkowity czas symulacji
        self.econ = econ                                    # czas działania serwera między przerwami
        self.ecoff = ecoff                                  # czas przerwy w działaniu serwera
        self.d = d                                          # średni czas obsługi wiadomości w serwerze
        self.zadanie = zadanie                              # numer zadania do wykonania

        self.minLiczbaZdarzen = 10                          # minimalna ilość zdarzeń w symulacji (ZMIENNA POMOCNICZA)
        self.tempLambda = 0.0                               # wartość lambda dla generatora zdarzeń (ZMIENNA POMOCNICZA)
        self.rozbieg = 10
