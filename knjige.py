import csv
import os
import re
import requests

# URL glavne spletne strani: Wikipedia
knjige_url = 'https://en.wikipedia.org/wiki/List_of_book-based_war_films_(1945%E2%80%932000_wars)'
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
    izraz = re.compile(r'<tr>.*?<td><i><a (.*?)</td></tr>', re.DOTALL)
    return [m.group(0) for m in re.finditer(izraz, page_content)]

# Da preverim delovanje te funkcije, vstavim npr. tole: niz = ' <tr><td><i><a href="/wiki/The_Red_Danube" title="The Red Danube">The Red Danube</a></i></td><td>1949</td><td><a href="/wiki/George_Sidney" title="George Sidney">George Sidney</a></td><td>US</td><td><i><a href="/wiki/Vespers_in_Vienna" title="Vespers in Vienna">Vespers in Vienna</a></i></td><td><a href="/wiki/Bruce_Marshall" title="Bruce Marshall">Bruce Marshall</a></td><td>1947</td><td>Novel</td></tr><tr>'

vzorec_filma = re.compile(
    r'<td><i><a.*?title=".*?">(?P<film>.*?)</a></i>.*?</td>.*?'
    r'<td>(?P<leto_filma>.*?)</td>.*?'
    r'<td>(.*?<a.*?title=".*?">)?(?P<reziser>.*?)(</a>.*?)?</td>.*?'
    r'<td>(<a href=".*?" title=".*?">)?(?P<drzave>.*?)(</a>)?</td>.*?'
    r'<td>(<i>)?(")?(<a.*?title=".*?">)?(?P<knjiga>.*?)(</a>)?(</i>|").*?</td>.*?'
    r'<td>(")?(<a.*?title=".*?">)?(?P<avtor>.*?)(</a>)?"?</td>.*?'
    r'<td>(?P<leto_izida_knjige>(\d\d\d)?.*?)</td>.*?'
    r'<td>(?P<zvrst>.*?)\n.*?</td></tr>'
    ,
    re.DOTALL
)

def get_dict_from_book_block(blok):
    """Funkcija iz niza za posamezno knjigo izlušči podatke o ........ imenu, ceni
    in opisu ter vrne slovar, ki vsebuje ustrezne podatke
    """
    izraz = vzorec_filma
    podatki = re.search(izraz, blok)
    slovar = podatki.groupdict()
    return slovar


#[get_dict_from_book_block(knjiga) for knjiga in page_to_books(read_file_to_string(mapa, 'filmi3.html'))]

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