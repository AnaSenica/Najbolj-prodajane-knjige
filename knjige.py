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

#[get_dict_from_book_block(knjiga) for knjiga in page_to_books(read_file_to_string(mapa, 'filmi3.html'))]



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
vzorec_brez_krnekej = re.compile(
    r'(.+?)&#160;: roman.*?',
    flags=re.DOTALL
)
def pomozna_funkcija1(film, kategorija):
    film = film
    if ' &amp; ' not in film[kategorija] and ', ' not in film[kategorija]:
        if '<a' not in film[kategorija]:
            film[kategorija] = [vzorec_brez_a.sub(r'\1', film[kategorija])]
            if '?' in film[kategorija][0]:
                film[kategorija][0] = film[kategorija][0].replace('?', '')
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
        elementi = re.split('/<br />', film[kategorija])
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
    for i in film[kategorija]:
        if '/' in i:
            elementi = re.split('/', i)
            film[kategorija] = [e for e in elementi]
    return film

def pomozna_funkcija_leto_knjige(film, kategorija):
    film = film
    if film[kategorija] == '?':
        film[kategorija] = None
    else:
        popravljene_letnice = film[kategorija].replace('?', '0')
        film[kategorija] = popravljene_letnice[:4]
    return film
    
def pomozna_funkcija_knjiga(film, kategorija):
    film = film
    if film[kategorija] == '?':
        film[kategorija] = None
    else:
        if '<sup' in film[kategorija]:
            film[kategorija] = film[kategorija][:5] + film[kategorija][-8:]
        elif '&#160;: roman' in film[kategorija]:
            film[kategorija] = vzorec_brez_krnekej.sub(r'\1', film[kategorija])
    return film




########################################################################

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


def popravi_podatke(blok):
    film = vzorec_filma.search(blok).groupdict()
    pomozna_funkcija1(film, 'drzave')
    pomozna_funkcija1(film, 'avtor')
    pomozna_funkcija1(film, 'reziser')
    pomozna_funkcija_zvrst(film, 'zvrst')
    pomozna_funkcija_leto_knjige(film, 'leto_izida_knjige')
    pomozna_funkcija_knjiga(film, 'knjiga')
    return film


def books_from_file(ime_datoteke, lokacija_datoteke):
    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
    pretvori (razčleni) v pripadajoč seznam slovarjev za vsako knjigo posebej."""
    stran = read_file_to_string(lokacija_datoteke, ime_datoteke)
    knjige = page_to_books(stran)
    seznam = [popravi_podatke(knjiga) for knjiga in knjige]
    return seznam


def zapisi_seznam_filmov():
    seznam = books_from_file(glavna_stran, mapa)
    nov_seznam = []
    for slovar in seznam:
        if slovar not in nov_seznam:
            nov_seznam.append(slovar)
        else:
            pass
    stevilo = 1
    for slovar in nov_seznam:
        slovar['id'] = stevilo
        stevilo += 1
    return nov_seznam



def izloci_gnezdene_podatke(filmi):
    reziser, avtor, zvrst, drzave = [], [], [], []
    for film in filmi:
        for z in film.pop('zvrst'):
            zvrst.append({'film_id': film['id'], 'zvrst': z})
        for a in film.pop('avtor'):
            avtor.append({'film_id': film['id'], 'avtor': a})
        for r in film.pop('reziser'):
            reziser.append({'film_id': film['id'], 'reziser': r})
        for d in film.pop('drzave'):
            drzave.append({'film_id': film['id'], 'drzave': d})
    return reziser, avtor, zvrst, drzave

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

#FILMI = zapisi_seznam_filmov()
#reziser, avtor, zvrst, drzave = izloci_gnezdene_podatke(FILMI)
#zapisi_csv(FILMI, ['id', 'film', 'leto_filma', 'knjiga', 'leto_izida_knjige'], 'filmi_po_knjigah.csv')
#zapisi_csv(reziser, ['film_id', 'reziser'], 'reziserji.csv')
#zapisi_csv(avtor, ['film_id', 'avtor'], 'avtorji_knjig.csv')
#zapisi_csv(zvrst, ['film_id', 'zvrst'], 'zvrsti_knjige.csv')
#zapisi_csv(drzave, ['film_id', 'drzave'], 'drzave.csv')