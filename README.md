# OAST_Project1 - Symulator zdarzeniowy kolejki M/M/1 – ON/OFF

Celem projektu jest napisanie symulatora systemu kolejki M/M/1, w którym serwer wyłącza się okresowo z obsługi przychodzących wiadomości. Zakładamy, że:

• czas działania serwera między przerwami jest modelowany zmienną losową Con o rozkładzie wykładniczym ze średnią E(Con)=40 [s]

• przerwy w działaniu serwera są niezależne od czasu jego działania i modelowane zmienną losową Coff o rozkładzie wykładniczym ze średnią E(Coff)=35 [s]

• obsługa zgłoszenia przerwana przez wyłączenie serwera zostaje dokończona po wznowieniu jego działania.

• średni czas obsługi wiadomości w serwerze D=0.125 [s]

Część I. Przetestować symulator dla zwykłej kolejki M/M/1 (bez wyłączeń). Przeprowadzić symulacje umożliwiające porównanie osiągniętych rezultatów z wynikami uzyskanymi z modelu analitycznego w zakresie wartości średniego opóźnienia w systemie E[T], przy założeniu średniej intensywności napływu λ od 0.5 do 6 [s-1] (zamieścić wyniki w postaci wykresu)

Część II. Przetestować symulator dla kolejki M/M/1 z wyłączeniami. Przeprowadzić symulacje umożliwiające porównanie osiągniętych rezultatów z wynikami uzyskanymi z następującej aproksymacji wartości średniego opóźnienia w systemie E[Ton/off]:

E[Ton/off] = [ ρ′ + λE[Coff]Poff ] / [ (1 − ρ′)λ ]

ρ′ = λ / μPon

przy założeniu średniej intensywności napływu λ od 0.5 do 4 [s-1] (zamieścić wyniki w postaci wykresu). Pon i Poff są prawdopodobieństwami odpowiednio: działania i niedziałania serwera.
