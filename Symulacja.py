from Kolejka import *
from System import *


class Symulacja:
    def __init__(self, ustawienia):
        self.ustawienia = ustawienia

        self.zdarzeniaWSystemie = 0
        self.zdarzeniaWKolejce = 0

        self.czasWSystemie = 0.0
        self.czasWKolejce = 0.0

        self.srednieOpoznienie = 0.0

        self.kolejka = Kolejka()   # pojedyncze zdarzenie generowane w konstruktorze kolejki
        self.system = System(self.kolejka, self.ustawienia)    # domyślnie pusty system

    def uruchom_MM1(self, lista_zdarzen):
        self.system.aktualizujStanSystemu()    # stan początkowy systemu
        while not lista_zdarzen.isEmpty():
            obecneZdarzenie = lista_zdarzen.get()
            self.system.obsluz(obecneZdarzenie)   # obsługa zdarzenia

            #if obecneZdarzenie.typ == 0:
            if obecneZdarzenie.typ == 'wiadomosc':
                self.kolejka.put(obecneZdarzenie)
                self.system.updateQueueStatistics()

        opoznienia = []
        for i in range(len(self.system.processedEvents)):   # obliczenie średniego opóźnienia z uwzględnieniem rozbiegu
            if self.system.processedEvents[i].t_przyjscia > self.ustawienia.rozbieg:
                opoznienia.append(self.system.processedEvents[i].t_wyjscia - self.system.processedEvents[i].t_przyjscia)
        self.srednieOpoznienie = sum(opoznienia) / len(opoznienia)

        self.system.aktualizujStanSystemu()
        return self.srednieOpoznienie
