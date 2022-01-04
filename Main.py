from Standard_Queue import StandardQueue
from Start_Stop_Queue import StartStopQueue

# Parametry początkowe symulacji
MAX_CZAS_SYMULACJI = 10000
lam = -1
while lam not in [1, 2, 3]:
    lam = int(input("\nProszę wprowadzić wartość lambda wybierając z {1,2,3}: "))
    if lam in [1, 2, 3]:
        print("lambda = " + str(lam))
    else:
        print("Wybrano nieprawidłową wartość lambda. Proszę spróbować ponownie.\n")
mi = 4
ro = lam / mi
acs = 0.0
obsluzonych_zdarzen = 0  # liczba obsluzonych zdarzen (Real)
czas_obslugi_imag = 0  # czas obslugi klientow IMAG (do prawdopodobienstwa)
czas_obslugi_real = 0  # czas obslugi klientow REAL (do klientow w systemie)
zdarzen_w_kolejce = 0
czasy_przyjscia = []
czasy_rozpoczecia = []
odst_mdz_zgl = 0
czas_p_zero = 0

# Uruchomienie symulacji
mode = -1
while mode not in [1, 2]:
    mode = int(input("\nWybierz rodzaj kolejki do symulacji, wpisując odpowiednią cyfrę, gdzie:\n"
                        "   1) Standardowa kolejka M/M/1  2) Kolejka M/M/1 Continuous Service: "))
    if mode == 1:
        wynik_standard = StandardQueue.run_standard
    elif mode == 2:
        wynik_continuous = StartStopQueue.run_start_stop
    else:
        print("Wprowadzono nieprawidłowy numer wyboru kolejki. Proszę spróbować ponownie.\n")
