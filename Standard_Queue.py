import numpy as np
import Event_List
import Methods

#todo IMHO wszystko jest źle i do wyjebania ale na razie nie ruszam -A
#todo zrobić
class StandardQueue:
    def __init__(self, lambada, mi, ro, acs, obsluzonych_zdarzen, czas_p_zero, czas_obslugi_real,
                 max_czas_symulacji, zdarzen_w_kolejce, czasy_przyjscia, czasy_rozpoczecia, odst_mdz_zgl):

        self.lambada = lambada
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

        self.event_list = list()
        self.list = Event_List.EventList(self.event_list)  # Obiekt listy zdarzen

        self.lista_czasow = list()
        self.ile_zdarzen = list()
        #todo zrozumieć co to jets
        self.odst_mdz_zgl = odst_mdz_zgl

##########################################
#jeśli w argumencie trzeba dać klasę Standard Queue albo StartStop to mija się z celem

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


#####################################################



    #todo progress status
    def progress(self):
        przekroczenie = self.acs >= self.max_czas_symulacji
        if przekroczenie:
            print("Zakończono symulację ze względu na przekroczenie czasu.")
            return True
        else:
            return False

#########################################

    def run_standard(self):

        print("\n\nZwykła Kolejka M/M/1(bez wyłączeń)\n")
        print("\tmi = " + str(self.mi))
        print("\tlambda = " + str(self.lambada))
        print("\tro = " + str(self.lambada / self.mi))
        print("\tmax czas symulacji = " + str(self.max_czas_symulacji))
        print("\nStart symulacji \n")

        #todo zrozumieć o co chodzi
        tz = ["PRZYJSCIE_REAL", "PRZYJSCIE_IMAG"]

        #todo sprawić by import Methods się zaświecił że połączony gen_t_obsługi
        self.lista.put(tz[0], 0, self.gen_t_obslugi(), self.gen_t_przyjscia())
        self.odst_mdz_zgl = self.lista_zdarzen[-1].t_nastepne

        while not self._zakoncz_symulacje():

            if self.lista_zdarzen[-1].t_przyjscia < self.max_czas_symulacji:
                self.lista.put(tz[0], self.odst_mdz_zgl, self.gen_t_obslugi(), self.gen_t_przyjscia())

            self.odst_mdz_zgl = self.lista_zdarzen[-1].t_nastepne + self.lista_zdarzen[-1].t_przyjscia
            self.lista.sortuj_liste(self.lista_zdarzen)
            zdarzen_w_kolejce = 0

            for i in range(len(self.lista_zdarzen)):
                if self.lista_zdarzen[i].t_przyjscia < self.acs:
                    zdarzen_w_kolejce += 1

            self.lista_czasow.append(self.acs)
            self.ile_zdarzen.append(zdarzen_w_kolejce)  # test

            if self.acs >= self.lista_zdarzen[0].t_przyjscia:

                zdarzenie = self.lista.get()  # Obsługuje zdarzenie, usuwam z listy zdarzeń
                zdarzen_w_kolejce -= 1
                self.obsluzonych_zdarzen += 1

                self.czas_obslugi_real += zdarzenie.t_obslugi

                self.czasy_przyjscia.append(zdarzenie.t_przyjscia)
                self.czasy_rozpoczecia.append(self.acs)

                self.acs += zdarzenie.t_obslugi  # Aktualny czas zwiększam o czas obsługi zdarzenia
            else:
                self.lista.put(tz[1], self.acs, self.gen_t_obslugi(), self.gen_t_przyjscia())   # dla ostatniego punktu zadania
                self.lista.sortuj_liste(self.lista_zdarzen)                                     # w put(): t_obslugi = 1/mi
                self.acs = self.lista_zdarzen[0].t_przyjscia                                    # MM1_CS_Wyniki_v2.txt

                zdarzenie = self.lista.get()

                self.czas_obslugi_imag += zdarzenie.t_obslugi
                self.acs += zdarzenie.t_obslugi