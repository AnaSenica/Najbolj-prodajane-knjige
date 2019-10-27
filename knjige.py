import csv
import os
import re
import requests

# URL glavne spletne strani: Wikipedia
knjige_url = 'https://en.wikipedia.org/wiki/List_of_best-selling_books#List_of_best-selling_individual_books'
# mapa, v katero bom shranila podatke
mapa = 'knjige'
# ime datoteke, v katero bom shranila glavno stran
glavna_stran = 'knjge_stran.html'
# ime CSV datoteke, v katero bom shranila podatke
csv_datoteka = 'knjige.csv'

def download_url_to_string(url):
    """Funkcija kot argument sprejme niz in puskuša vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanjem pride do napake, vrne None.
    """
    try:
        page_content = requests.get(url).text
    except requests.exceptions.RequestException as e:
        print(e)
        page_content = ''
    return page_content

def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""
    content = download_url_to_string(page)
    save_string_to_file(content, directory, filename)
    return

#save_frontpage(knjige_url, mapa, glavna_stran)
#####################################################################################
# od tu naprej moram popraviti
#####################################################################################
# page_to_ads = page_to_books
# get_dict_from_ad_block = get_dict_from_book_block
# ads_from_file = books_from_file
# ads_frontpage = books_frontpage

def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf8') as datoteka1:
        return datoteka1.read()


def page_to_books(page_content):
    """Funkcija poišče posamezne knjige, ki se nahajajo v spletni strani in
    vrne njih seznam"""
    # (.*?) pomeni katerikoli znak, od 0 naprej, ? pomeni, da ni požrešen način. Torej pobere čim manj, kolikor je možno.
    # modul .DOTALL na knjižnici re poskrbi, da pika pomeni katerikoli znak, tudi presledke (če ni dotall, pika pomeni katerikoli znak razen presledkov)
    izraz = re.compile(r'<div class="ad">(.*?)<div class="clear">', re.DOTALL)
    return [m.group(0) for m in re.finditer(izraz, page_content)]

# Da preverim delovanje te funkcije, vstavim npr. tole: niz = ' <div class="ad"><div class="clear"></div></div><div class="ad"><div class="coloumn image"><td><a titl<div class="clear">'

# Definirajte funkcijo, ki sprejme niz, ki predstavlja oglas, in izlušči
# podatke o imenu, ceni in opisu v oglasu.


def get_dict_from_book_block(blok):
    """Funkcija iz niza za posamezno knjigo izlušči podatke o ........ imenu, ceni
    in opisu ter vrne slovar, ki vsebuje ustrezne podatke
    """
    izraz = re.compile(
        r'<h3><a title="(?P<ime>.*?)"'
        r'.*?>(?P<opis>.*?)</a></h3>'
        r'.*?class="price">(<span>)?(?P<cena>.*?)( €</span>)?</div',
        re.DOTALL
    )
    podatki = re.search(izraz, blok)
    # .groupdict() vrne slovar POIMENOVANIH spremenljivk 
    slovar = podatki.groupdict()
    return slovar

# Da preverim delovanje te funkcije, vstavim npr. tole:
#'<span class="flag_newAd"></span>         </div><div class="coloumn content"><h3><a title="Gusarka Loti (DZZŽ Kranj)" href="http://www4103">Gusarka Loti (DZZŽ Kranj)</a></h3><div class="price">Po dogovoru</div>  <div class="clear"></div>  <div class="miscellaneous">'



# Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
# besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
# vseh oglasih strani.


def books_from_file(ime_datoteke, lokacija_datoteke):
    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
    pretvori (razčleni) v pripadajoč seznam slovarjev za vsako knjigo posebej."""
    stran = read_file_to_string(lokacija_datoteke, ime_datoteke)
    knjige = page_to_books(stran)
    seznam = [get_dict_from_book_block(knjiga) for knjiga in knjige]
    return seznam

def books_frontpage():
    return books_from_file(glavna_stran, mapa)