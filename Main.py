from Ustawienia import *
from Symulacja import *

#todo spolszczyć
#todo dodać drukowanie do pliku

def dopliku(tempLambda, mean):
    plik = open('wyniki.txt', 'a')
    plik.write(f'{tempLambda} ; {mean} \n')
    plik.close()


def main():
    zadanie = 1
    seed = 128
    open('wyniki.txt', 'w').close() # czyszczenie pliku z wynikami

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
    tempLambda = ustawienia.minLambda

    while tempLambda <= ustawienia.maxLambda:  # symulacje dla wielu wartości lambda
        meanDelaySystemTimeSum = 0.0  # wartość średniego opóźnienia w systemie E[T]

        print("\nAktualna wartość Lambda:", tempLambda)
        for i in range(ustawienia.liczbaSymulacji):  # symulacje powtarzamy wielokrotnie
            ustawienia.tempLambda = tempLambda
            lista_zdarzen = ListaZdarzen()
            generator = Generator(ustawienia)
            generator.generuj(lista_zdarzen)
            lista_zdarzen.print_list()
            symulacja = Symulacja(ustawienia)
            meanDelaySim = symulacja.uruchom_MM1(lista_zdarzen)
            meanDelaySystemTimeSum += meanDelaySim
            np.random.seed(ustawienia.seed + 2137 * i)  # zmiana ziarna po każdej symulacji
            print("Symulacja nr: {}, E[T] w aktualnej symulacji: {}\n".format(i + 1, meanDelaySim))
            print("_________________________________________________________________________________________________________\n")
        print("E[T] dla danej wartości Lambda:", meanDelaySystemTimeSum / ustawienia.liczbaSymulacji)
        dopliku(tempLambda, meanDelaySystemTimeSum / ustawienia.liczbaSymulacji)
        tempLambda += 0.25


main()
