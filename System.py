from Lista_Zdarzen import *
import numpy as np


class Generator:
    def __init__(self, ustawienia):
        self.ustawienia = ustawienia

    def generujZdarzeniePoisson(self, srednia):
        return -np.log(1 - np.random.random()) / srednia

    def generujCzasWiadomosci(self):
        return self.generujZdarzeniePoisson(self.ustawienia.tempLambda)

    def generuj(self, lista_zdarzen):
        self.generujWiadomosci(lista_zdarzen)
        if self.ustawienia.wylaczanie:
            self.generujZdarzeniaPrzelaczania(lista_zdarzen)

        #e = Zdarzenie(3, self.ustawienia.dlugoscSymulacji, 0)  # na końcu generowane zdarzenie typu 3 - koniec
        e = Zdarzenie('koniec', self.ustawienia.dlugoscSymulacji, 0)  # na końcu generowane zdarzenie typu 3 - koniec
        lista_zdarzen.put(e)
        return lista_zdarzen

    def generujWiadomosci(self, lista_zdarzen):     # generator zdarzeń typu 0
        czas = self.generujCzasWiadomosci()
        if self.ustawienia.minLiczbaZdarzen:
            liczba_wiadomosci = self.ustawienia.minLiczbaZdarzen
            while liczba_wiadomosci != 0:
                #zdarzenie = Zdarzenie(0, czas, self.generujZdarzeniePoisson(1 / self.ustawienia.d))
                zdarzenie = Zdarzenie('wiadomosc', czas, self.generujZdarzeniePoisson(1 / self.ustawienia.d))
                lista_zdarzen.put(zdarzenie)

                czas += self.generujCzasWiadomosci()
                liczba_wiadomosci -= 1

            while czas < self.ustawienia.dlugoscSymulacji:
                #zdarzenie = Zdarzenie(0, czas, self.generujZdarzeniePoisson(1 / self.ustawienia.d))
                zdarzenie = Zdarzenie('wiadomosc', czas, self.generujZdarzeniePoisson(1 / self.ustawienia.d))
                lista_zdarzen.put(zdarzenie)

                czas += self.generujCzasWiadomosci()

    def generujZdarzeniaPrzelaczania(self, lista_zdarzen):  # generator zdarzeń typu 1 i 2
        czas = self.generujZdarzeniePoisson(1 / self.ustawienia.econ)
        wlaczony = True
        while czas < self.ustawienia.dlugoscSymulacji:
            if wlaczony:
                #zdarzenie = Zdarzenie(2, czas, 0)
                zdarzenie = Zdarzenie('serwer_off', czas, 0)
                czas += self.generujZdarzeniePoisson(1 / self.ustawienia.ecoff)
                wlaczony = False
            else:
                #zdarzenie = Zdarzenie(1, czas, 0)
                zdarzenie = Zdarzenie('serwer_on', czas, 0)
                czas += self.generujZdarzeniePoisson(1 / self.ustawienia.econ)
                wlaczony = True

            lista_zdarzen.put(zdarzenie)


class System:
    def __init__(self, kolejka, ustawienia):
        self.kolejkaZdarzen = kolejka
        self.ustawienia = ustawienia

        self.obecnyCzas = 0.0
        self.obecnyCzasSystemu = 0.0
        self.stan = 1
        self.t_wyl = 0.0 #czas wyłącz
        self.t_wl = 0.0 #czas włącz

        self.systemEvent = None
        self.remainingProcessingTime = 0.0
        self.timeIdle = 0.0
        self.timeProcessing = 0.0

        self.processedEvents = []
        self.queueEvents = []
        self.systemEvents = []
        self.systemState = []

    def obsluz(self, obecne_zdarzenie):
        self.obecnyCzas = obecne_zdarzenie.t_przyjscia
        self.doProcessing()
        self.obecnyCzasSystemu = self.obecnyCzas
        #if obecne_zdarzenie.typ == 1:     # obsługa włączeń i wyłączeń serwera
        if obecne_zdarzenie.typ == 'serwer_on':
            self.stan = 1
            self.aktualizujStanSystemu()
        #elif obecne_zdarzenie.typ == 2:
        elif obecne_zdarzenie.typ == 'serwer_off':
            self.stan = 2
            self.aktualizujStanSystemu()

    def doProcessing(self):
        uplywCzasu = self.obecnyCzas - self.obecnyCzasSystemu
        if self.stan == 2:
            self.t_wyl += uplywCzasu
            return
        else:
            self.t_wl += uplywCzasu

        while self.obecnyCzasSystemu < self.obecnyCzas:  # obsługa zdarzenia
            self.processEvent()

    def processEvent(self):
        if self.systemEvent is None:
            self.systemEvent = self.kolejkaZdarzen.get()
            if self.systemEvent is not None:
                self.remainingProcessingTime = self.systemEvent.t_obslugi

            self.updateSystemEvents()
            self.updateQueueStatistics()

        if self.systemEvent is None:    # jeśli zdarzenie jest null, tzn. że kolejka jest pusta i nic się nie wydarzyło
            self.timeIdle += self.obecnyCzas - self.obecnyCzasSystemu
            self.obecnyCzasSystemu = self.obecnyCzas
            self.updateSystemEvents()
            return

        self.obecnyCzasSystemu += self.remainingProcessingTime

        if self.obecnyCzasSystemu < self.obecnyCzas:   # zdarzenie obsłużone
            self.systemEvent.t_wyjscia = self.obecnyCzasSystemu
            self.processedEvents.append(self.systemEvent)
            self.systemEvent = None
            self.timeProcessing += self.remainingProcessingTime
        else:   # zdarzenie częściowo obsłużone
            self.timeProcessing += (self.remainingProcessingTime - (self.obecnyCzasSystemu - self.obecnyCzas))
            self.remainingProcessingTime = self.obecnyCzasSystemu - self.obecnyCzas
            self.obecnyCzasSystemu = self.obecnyCzas

    def updateQueueStatistics(self):        # jeśli size się zwiększa tzn. że do kolejki wchodzi zdarzenia; jeśli size się zmniejsza tzn. że z kolejki wychodzi zdarzenie
        self.queueEvents.append((self.obecnyCzasSystemu, self.kolejkaZdarzen.size()))

    def aktualizujStanSystemu(self):            # jeśli stan 1 - włączenie systemu; jeśli stan 2 - wyłączenie systemu
        self.systemState.append((self.obecnyCzasSystemu, self.stan))

    def updateSystemEvents(self):           # brak uaktualnień kiedy system jest OFF
        if self.systemEvent is None:
            x = 0
        else:
            x = 1
        self.systemEvents.append((self.obecnyCzasSystemu, x))


