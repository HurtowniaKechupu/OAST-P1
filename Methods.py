import numpy as np

#todo wszystko self musi być parametrem
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