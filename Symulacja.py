from Kolejka import *
from System import *

#todo spolszczyć
class Symulacja:
    def __init__(self, ustawienia):
        self.ustawienia = ustawienia

        self.zdarzeniaWSystemie = 0
        self.zdarzeniaWKolejce = 0

        self.czasWSystemie = 0.0
        self.czasWKolejce = 0.0

        self.srednieOpoznienie = 0.0

        self.kolejka = Kolejka()   # pojedyncze zdarzenie generowane w konstruktorze kolejki
        self.system = System(self.kolejka, self.ustawienia)    # system (serwer) jest domyślnie pusty

    def run_MM1(self, lista_zdarzen):
        self.system.aktualizujStanSystemu()    # stan początkowy systemu
        while not lista_zdarzen.isEmpty():
            currentEvent = lista_zdarzen.get()
            self.system.obsluz(currentEvent)   # obsługa zdarzenia

            if currentEvent.typ == 0:
                self.kolejka.put(currentEvent)
                self.system.updateQueueStatistics()

        times = []
        for i in range(len(self.system.processedEvents)):   # obliczenie średniego opóźnienia z uwzględnieniem rozbiegu
            if self.system.processedEvents[i].t_przyjscia > self.ustawienia.rozbieg:
                times.append(self.system.processedEvents[i].t_wyjscia - self.system.processedEvents[i].t_przyjscia)
        self.srednieOpoznienie = sum(times) / len(times)

        self.system.aktualizujStanSystemu()
        return self.srednieOpoznienie
