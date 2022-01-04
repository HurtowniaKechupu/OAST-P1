import numpy as np

import Event_List


class Queue:
    def __init__(self, lam, mi, ro, acs, obsluzonych_zdarzen, czas_p_zero, czas_obslugi_real,
                 max_czas_symulacji, zdarzen_w_kolejce, czasy_przyjscia, czasy_rozpoczecia, odst_mdz_zgl):

        # todo zangielszczyć
        self.lam = lam
        self.mi = mi
        self.ro = ro
        self.acs = acs

        self.obsluzonych_zdarzen = obsluzonych_zdarzen
        self.czas_p_zero = czas_p_zero
        self.czas_obslugi_real = czas_obslugi_real
        self.zdarzen_w_kolejce = zdarzen_w_kolejce

        self.max_czas_symulacji = max_czas_symulacji
        self.czasy_przyjscia = czasy_przyjscia
        self.czasy_rozpoczecia = czasy_rozpoczecia

        self.lista_zdarzen = list()
        self.lista = Event_List.EventList(self.lista_zdarzen)  # Obiekt listy zdarzen

        self.lista_czasow = list()
        self.ile_zdarzen = list()

        self.odst_mdz_zgl = odst_mdz_zgl

##############################
    # Metody generujace losowe czasy i liczące niezbędne parametry
    #todo zangielszczyć to
    def gen_t_obslugi(self):
        return -np.log(1 - np.random.random()) / self.mi

    def gen_t_przyjscia(self):
        return -np.log(1 - np.random.random()) / self.lam

    def obl_sr_licz_kl_w_buf(self):
        suma = 0
        for i in range(len(self.ile_zdarzen) - 1):
            suma += ((self.lista_czasow[i + 1] - self.lista_czasow[i]) * self.ile_zdarzen[i])
        return suma / self.acs

    def obl_sr_licz_kl_w_sys(self):
        wynik = self.obl_sr_licz_kl_w_buf() + self.czas_obslugi_real / self.acs
        return wynik

    def obl_sr_czas_ocz_na_obs(self):
        suma = 0
        for i in range(self.obsluzonych_zdarzen):
            suma += (self.czasy_rozpoczecia[i] - self.czasy_przyjscia[i])
        return suma / self.obsluzonych_zdarzen

    def obl_sr_czas_przej_przez_sys(self):
        suma = 0
        for i in range(self.obsluzonych_zdarzen):
            suma += (self.czasy_rozpoczecia[i] - self.czasy_przyjscia[i] + 1 / self.mi)
        return suma / self.obsluzonych_zdarzen

    ###########################################

    # todo zrozumieć i sprawić by robiłlo co trzeba
    def run_standard(self):
        print("\n\nKolejka M/M/1 - Standardowa\n")
        print("\tmi = " + str(self.mi))
        print("\tlambda = " + str(self.lam))
        print("\tro = " + str(self.lam / self.mi))
        print("\tmax czas symulacji = " + str(self.max_czas_symulacji))
        print("\nRozpoczynam symulację... \n")

        tz = ["PRZYJSCIE_REAL", "PRZYJSCIE_IMAG"]

        self.lista.put(tz[0], 0, self.gen_t_obslugi(), self.gen_t_przyjscia())
        self.odst_mdz_zgl = self.lista_zdarzen[-1].t_next

        while not self._zakoncz_symulacje():

            if self.lista_zdarzen[-1].t_arrival  < self.max_czas_symulacji:
                self.lista.put(tz[0], self.odst_mdz_zgl, self.gen_t_obslugi(), self.gen_t_przyjscia())

            self.odst_mdz_zgl = self.lista_zdarzen[-1].t_next + self.lista_zdarzen[-1].t_arrival
            self.lista.sort_list(self.lista_zdarzen)
            zdarzen_w_kolejce = 0

            for i in range(len(self.lista_zdarzen)):
                if self.lista_zdarzen[i].t_arrival < self.acs:
                    zdarzen_w_kolejce += 1

            self.lista_czasow.append(self.acs)
            self.ile_zdarzen.append(zdarzen_w_kolejce)  # test

            if self.acs >= self.lista_zdarzen[0].t_arrival:

                zdarzenie = self.lista.get()  # Obsługuje zdarzenie, usuwam z listy zdarzeń
                zdarzen_w_kolejce -= 1
                self.obsluzonych_zdarzen += 1

                self.czas_obslugi_real += zdarzenie.t_handling

                self.czasy_przyjscia.append(zdarzenie.t_arrival)
                self.czasy_rozpoczecia.append(self.acs)

                self.acs += zdarzenie.t_handling  # Aktualny czas zwiększam o czas obsługi zdarzenia
            else:
                self.lista.sort_list(self.lista_zdarzen)
                self.czas_p_zero += self.lista_zdarzen[0].t_arrival - self.acs  # licze czas trwania stanu p0
                self.acs = self.lista_zdarzen[0].t_arrival  # aktualny czas = czas przyjscia nastepnego zdarzenia


        # todo to może przerobić na metodę z argumentem
        # Wyświetlenie wyników
        # E[W] = Wq; E[T] = W; E[Q] = Lq; E[N] = L
        print("-"*40 + "\n\nŚredni czas oczekiwania na obsługę E[W] = "
              + str(self.obl_sr_czas_ocz_na_obs())
              + "\t[Teoretycznie: Wq = " + str(self.ro ** 2 / (self.lam * (1 - self.ro))) + "]\n"

              + "Średni czas przejścia przez system E[T] = "
              + str(self.obl_sr_czas_przej_przez_sys())
              + "\t[Teoretycznie: W = " + str(self.ro / (self.lam * (1 - self.ro))) + "]\n"

              + "Średnia liczba klientów w buforze  E[Q] = "
              + str(self.obl_sr_licz_kl_w_buf())
              + "\t[Teoretycznie: Lq = " + str(self.ro ** 2 / (1 - self.ro)) + "]\n"

              + "Średnia liczba klientów w systemie E[N] = "
              + str(self.obl_sr_licz_kl_w_sys())
              + "\t[Teoretycznie: L = " + str(self.ro / (1 - self.ro)) + "]\n"

              + "Prawdopodobieństwo p0 = "
              + str(self.czas_p_zero / self.acs) + "\n\n" + "-"*40)

        # Zapis do pliku
        do_pliku = open("MM1_Standard_Wyniki.txt", 'a')

        do_pliku.write("-" * 10 + " DANE SYMULACJI " + "-" * 10 + "\n\n"
                       + "\tmi = " + str(self.mi) + "\n"
                       + "\tlam = " + str(self.lam) + "\n"
                       + "\tro = " + str(self.lam / self.mi) + "\n"
                       + "\tmax czas symulacji = " + str(self.max_czas_symulacji) + "\n\n"

                       + "-" * 10 + " WYNIKI SYMULACJI - M/M/1 STANDARD QUEUE " + "-" * 10 + "\n\n"
                       + "Średni czas oczekiwania na obsługę E[W] = "
                       + str(self.obl_sr_czas_ocz_na_obs())
                       + "\t[Teoretycznie: Wq = " + str(self.ro ** 2 / (self.lam * (1 - self.ro))) + "]\n"

                       + "Średni czas przejścia przez system E[T] = "
                       + str(self.obl_sr_czas_przej_przez_sys())
                       + "\t[Teoretycznie: W = " + str(self.ro / (self.lam * (1 - self.ro))) + "]\n"

                       + "Średnia liczba klientów w buforze  E[Q] = "
                       + str(self.obl_sr_licz_kl_w_buf())
                       + "\t[Teoretycznie: Lq = " + str(self.ro ** 2 / (1 - self.ro)) + "]\n"

                       + "Średnia liczba klientów w systemie E[N] = "
                       + str(self.obl_sr_licz_kl_w_sys())

                       + "\t[Teoretycznie: L = " + str(self.ro / (1 - self.ro)) + "]\n"
                       + "Prawdopodobieństwo p0 = " + str(self.czas_p_zero / self.acs) + "\n\n")

    def _zakoncz_symulacje(self):
        przekroczenie = self.acs >= self.max_czas_symulacji
        if przekroczenie:
            print("Zakończono symulację ze względu na przekroczenie czasu.")
            return True
        else:
            return False

    def run_start_stop(self):
        #todo zrobic
        return "dupa"