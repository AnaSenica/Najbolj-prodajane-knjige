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
    r'(?P<drzave><td>(<a href=".*?" title=".*?">)?.*?(</a>)?</td>.*?)'
    r'<td>(<i>)?(")?(<a.*?title=".*?">)?(?P<knjiga>.*?)(</a>)?(</i>|").*?</td>.*?'
    r'(?P<avtor><td>(")?(<a.*?title=".*?">)?.*?(</a>)?"?</td>.*?)'
    r'<td>(?P<leto_izida_knjige>(\d\d\d)?.*?)</td>.*?'
    r'<td>(?P<zvrst>.*?)\n.*?</td></tr>'
    ,
    re.DOTALL
)



#def get_dict_from_book_block(blok):
#    """Funkcija iz niza za posamezno knjigo izlušči podatke o ........ imenu, ceni
#    in opisu ter vrne slovar, ki vsebuje ustrezne podatke
#    """
##    izraz = vzorec_filma
 #   podatki = re.search(izraz, blok)
 #   slovar = podatki.groupdict()
  #  return slovar


#[get_dict_from_book_block(knjiga) for knjiga in page_to_books(read_file_to_string(mapa, 'filmi3.html'))]

# Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
# besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
# vseh oglasih strani.

def books_frontpage():
    return books_from_file(glavna_stran, mapa)




def books_from_file(ime_datoteke, lokacija_datoteke):
    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
    pretvori (razčleni) v pripadajoč seznam slovarjev za vsako knjigo posebej."""
    stran = read_file_to_string(lokacija_datoteke, ime_datoteke)
    knjige = page_to_books(stran)
    seznam = [popravi_podatke(knjiga) for knjiga in knjige]
    return seznam

def mala_books_frontpage():
    return books_from_file('filmi3.html', mapa)

#mala_books_frontpage()
#books_from_file('filmi3.html', mapa)


vzorec_z_a = re.compile(
    r'<td>.*?<a .*?>(.+?)</a>.*?(</td>)?\n',
    flags=re.DOTALL
)
vzorec_brez_a = re.compile(
    r'<td>(.+?)</td>\n',
    flags=re.DOTALL
)
vzorec_brez_a_konec = re.compile(
    r'(.+?)</td>\n',
    flags=re.DOTALL
)
vzorec_z_a_konec = re.compile(
    r'<a.*?>(.+?)</a>.*?</td>\n',
    flags=re.DOTALL
)
vzorec_brez_a_zacetek = re.compile(
    r'<td>(.+?)',
    flags=re.DOTALL
)
vzorec_z_a_zacetek = re.compile(
    r'<td>(<a .*?>.*?</a>.*?)?.*?<a .*?>(.+?)</a>(.*)?',
    flags=re.DOTALL
)
vzorec_z_a_sredina = re.compile(
    r'<a .*?>(.+?)</a>',
    flags=re.DOTALL
)
poseben_vzorec_drzave = re.compile(
    r'<td>(.+?)<sup.*?><a .*?>.*?</a>.*?(</td>)?\n',
    flags=re.DOTALL
)
vzorec_brez_b = re.compile(
    r'<b>(.+?)</b>',
    flags=re.DOTALL
)
vzorec_brez_sup = re.compile(
    r'(.+?)<sup.*?>.*?</sup>',
    flags=re.DOTALL
)

def pomozna_funkcija1(film, kategorija):
    film = film
    if ' &amp; ' not in film[kategorija]:
        if '<a' not in film[kategorija]:
            film[kategorija] = [vzorec_brez_a.sub(r'\1', film[kategorija])]
        else:
            if kategorija == 'drzave' and '<sup' in film[kategorija]:
                film[kategorija] = [poseben_vzorec_drzave.sub(r'\1', film[kategorija])]
            else:
                film[kategorija] = [vzorec_z_a.sub(r'\1', film[kategorija])]
    else:
        seznam = []
        elementi = re.split(', | &amp; ', film[kategorija])
        for e in elementi:
            if '<td>' in e:
                if '<a' not in e:
                    seznam.append(vzorec_brez_a_zacetek.sub(r'\1', e))
                else:
                    seznam.append(vzorec_z_a_zacetek.sub(r'\2', e))
            elif '</td>' in e:
                if '<a' not in e:
                    seznam.append(vzorec_brez_a_konec.sub(r'\1', e))
                else:
                    seznam.append(vzorec_z_a_konec.sub(r'\1', e))
            else:
                if '<a'  in e:
                    seznam.append(vzorec_z_a_sredina.sub(r'\1', e))
                else:
                    seznam.append(e)
        film[kategorija] = seznam
    return film

def pomozna_funkcija_zvrst(film, kategorija):
    film = film
    if '/<br />' in film[kategorija]:
        elementi = re.split('/<br />|/', film[kategorija])
        film[kategorija] = [e for e in elementi]
    else:
        film[kategorija] = [film[kategorija]]
    for e in film[kategorija]:
        seznam = []
        if '<b>' in e:
            seznam.append(vzorec_brez_b.sub(r'\1', e))
        elif '<sup' in e:
            seznam.append(vzorec_brez_sup.sub(r'\1', e))
        elif '<a' in e:
            seznam.append(vzorec_z_a_sredina.sub(r'\1', e))
        else:
            seznam.append(e)
        film[kategorija] = seznam
    return film

def pomozna_funkcija_leto_knjige(film, kategorija):
    film = film
    if film[kategorija] == '?':
        film[kategorija] = None
    else:
        popravljene_letnice = film[kategorija].replace('?', '0')
        film[kategorija] = popravljene_letnice[:4]
    return film


    

########################################################################
def popravi_podatke(blok):
    film = vzorec_filma.search(blok).groupdict()
    pomozna_funkcija1(film, 'drzave')
    pomozna_funkcija1(film, 'avtor')
    pomozna_funkcija1(film, 'reziser')
    pomozna_funkcija_zvrst(film, 'zvrst')
    pomozna_funkcija_leto_knjige(film, 'leto_izida_knjige')
    print(film['leto_izida_knjige'])
    #return film

