from Ustawienia import *
from Symulacja import *
from Statistics import *

#todo spolszczyć
#todo dodać drukowanie do pliku
def generate_eventList(ustawienia, lambda2):   # generacja listy zdarzeń
    ustawienia.tempLambda = lambda2
    lista_zdarzen = ListaZdarzen()
    generator = Generator(ustawienia)
    generator.generuj(lista_zdarzen)
    lista_zdarzen.print_list()
    return lista_zdarzen


def print_states(x, y, z):
    print("Zmiany stanu systemu (self.obecnyCzasSystemu, self.stan): {}\n"
          "Zdarzenia w systemie (self.obecnyCzasSystemu, self.systemEvent is None ? 0 : 1): {}\n"
          "Zdarzenia w kolejce (self.obecnyCzasSystemu, self.kolejkaZdarzen.size()): {}"
          .format(x, y, z))


def main():
    zadanie = 1
    seed = 128

    if zadanie == 1:
        minLambda = 0.5
        maxLambda = 6
        liczbaSymulacji = 20
        dlugoscSymulacji = 500
        wylaczanie = False
    elif zadanie == 2:
        minLambda = 0.5
        maxLambda = 4
        liczbaSymulacji = 2
        dlugoscSymulacji = 50000
        wylaczanie = True
    else:
        print("Błedny numer zadania!")
        return 1

    ustawienia = Ustawienia(minLambda=minLambda,
                        maxLambda=maxLambda,
                        seed=seed,
                        wylaczanie=wylaczanie,
                        liczbaSymulacji=liczbaSymulacji,
                        dlugoscSymulacji=dlugoscSymulacji,
                        econ=40,
                        ecoff=35,
                        d=0.125,
                        zadanie=zadanie)

    print("Symulator kolejki M/M/1 - Zadanie", zadanie)
    np.random.seed(ustawienia.seed)
    statistics = Statistics(ustawienia)
    tempLambda = ustawienia.minLambda

    while tempLambda <= ustawienia.maxLambda:  # symulacje dla wielu wartości lambda
        meanDelaySystemTimeSum = 0.0  # wartość średniego opóźnienia w systemie E[T]

        print("\nAktualna wartość Lambda:", tempLambda)
        for i in range(ustawienia.liczbaSymulacji):  # symulacje powtarzamy wielokrotnie
            lista_zdarzen = generate_eventList(ustawienia, tempLambda)
            symulacja = Symulacja(ustawienia)
            meanDelaySim = symulacja.run_MM1(lista_zdarzen)
            meanDelaySystemTimeSum += meanDelaySim
            np.random.seed(ustawienia.seed + 2137 * i)  # zmiana ziarna po każdej symulacji
            print("Symulacja nr: {}, E[T] w aktualnej symulacji: {}\n".format(i + 1, meanDelaySim))
            print_states(symulacja.system.systemState, symulacja.system.systemEvents, symulacja.system.queueEvents)
            print("------------------------------------------------------------------------------------------------------------------------------------\n")
        print("E[T] dla danej wartości Lambda:", meanDelaySystemTimeSum / ustawienia.liczbaSymulacji)
        statistics.addStatistics(meanDelaySystemTimeSum / ustawienia.liczbaSymulacji, tempLambda)
        tempLambda += 0.25

    statistics.plot()

main()
