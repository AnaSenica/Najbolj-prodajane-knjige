# Vojni filmi, posneti po knjigah
Repozitorij za projektno nalogo pri predmetu Programiranje 1

Analizirala bom seznam vojnih filmov, posnetih po knjižni predlogi, glede na [Wikipedijo](https://en.wikipedia.org/wiki/List_of_book-based_war_films_(1945%E2%80%932000_wars))

Za vsak film bom zajela:
* naslov
* ime režiserja
* leto izida
* knjižno predlogo
* leto izida knjige
* ime avtorja knjige

Delovne hipoteze:
* Katera zvrst knjige je njabolj primerna za predelavo v film?
* Katera država je posnela največ vojnih filmov?
* V katerem obdobju so posneli največ vojnih filmov po knjižni predlogi?
* Koliko let mine od izida knjige do izida filmske predelave?

Podatki, pripravljeni za analizo, so v CSV datotekah: filmi_po_knjigah.csv vsebuje filme, knjige, po katerih so bili posneti in letnice izida filmov in knjig; drzave.csv vsebuje države, v katerih je bil film posnet; avtorji_knjig.csv in reziserji.csv vsebujeta vse pisatelje in režiserje, ki so sodelovali pri filmu ali knjigi; zvrsti_knjige.csv vsebuje zvrsti knjig, po katerih so bili posneti filmi. Podatki so indeksirani glede na film, h kateremu sodijo.
V knjige.py je koda, ki sem jo uporabila za zajem podatkov.

(Moja prvotna tema je bila Najbolj prodajane knjige, a sem ugotovila, da je bilo knjig na seznamu premalo, zato sem temo spremenila.)