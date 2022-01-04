from Queue import Queue


# Parametry początkowe
MAX_CZAS_SYMULACJI = 10000

lam = -1.0
#todo ogarnąć mi, czemu jest na sztywno 4?
mi = 4
ro = lam / mi
acs = 0.0

#todo zangielszczyć to gówno
obsluzonych_zdarzen = 0  # liczba obsluzonych zdarzen (Real)
czas_obslugi_imag = 0  # czas obslugi klientow IMAG (do prawdopodobienstwa)
czas_obslugi_real = 0  # czas obslugi klientow REAL (do klientow w systemie)
zdarzen_w_kolejce = 0
czasy_przyjscia = []
czasy_rozpoczecia = []
odst_mdz_zgl = 0
czas_p_zero = 0

# Uruchomienie symulacji
mode = "-1.0"
while True:
    mode = input("\nWybierz rodzaj kolejki:\n"
                        "   1) Zwykła kolejka M/M/1 (bez wyłączeń)  2) Kolejka M/M/1 z wyłączeniami: ")
    if mode =="1" or mode=="2":
        break
    else:
        print("Wprowadzono nieprawidłowy numer wyboru kolejki. Proszę spróbować ponownie.\n")

while True:
    #todo naprawić to
    #lam = float(input("\nPodaj wartość lambda z przedziału [0.5, 6] [s^-1]: "))
    lam =3.0
    if 6.0 >= lam >= 0.5:
        print("lambda = " + str(lam))
        break
    else:
        print("Podano nieprawidłową wartość lambda. Proszę spróbować ponownie.\n")

# todo zangielszczyć to gówno
queue = Queue(
    lam=lam,
    mi=mi,
    ro=ro,
    acs=acs,
    obsluzonych_zdarzen=obsluzonych_zdarzen,
    czas_p_zero=czas_p_zero,
    czas_obslugi_real=czas_obslugi_real,
    max_czas_symulacji=MAX_CZAS_SYMULACJI,
    zdarzen_w_kolejce=zdarzen_w_kolejce,
    czasy_przyjscia=czasy_przyjscia,
    czasy_rozpoczecia=czasy_rozpoczecia,
    odst_mdz_zgl=odst_mdz_zgl
)

if mode == "1":
    #todo sprawdzić czy się zgadza z poleceniem
    result_standard = queue.run_standard()
elif mode == "2":
    #todo zaimplementować
    result_start_stop = queue.run_start_stop()
