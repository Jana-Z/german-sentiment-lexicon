from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import re
import requests
from bs4 import BeautifulSoup

from fundementals import convert_umlaute, \
    count_words, capitalize
from manage_files import *

def main():
    emotionlist = ['ekel', 'furcht', 'trauer', 'überraschung', 'verachtung', 'wut', 'freude', 'liebe']

    get_first_degree_assosiactions('./emotions/', emotionlist)
    get_second_degree_assosiactions('./emotions/', emotionlist)

def get_assosications_from_wordassociations(word):
    # needs umlaute to work
    url = 'https://wordassociations.net/de/assoziationen-mit-dem-wort/' + word
    print(f'scraping {url}')

    links = []
    i = 0

    while i <= 300:
        new_url = url + '?=start=' + str(i)
        page = requests.get(new_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        sections = soup.find_all("div", class_="section")
        if sections is not None:
            for section in sections:
                links.extend(section.find_all('a', href=True))
        i += 100
        
    return set([link.text.strip() for link in links])

def get_assosications_from_dwds(word):
    # nouns have to be capitalized and with umlauten
    word = capitalize(word)

    url = 'https://www.dwds.de/wp?q=' + word + '&comp-method=diff&comp=&pos=2&minstat=0&minfreq=5&by=logDice&limit=100&view=table'
    print(f'scraping {url}')

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    spans = []

    ueberblick = soup.find(id=re.compile('.*-22$'))
    if ueberblick is not None:
        spans.extend(ueberblick.find_all('span', class_='wp-rel'))

    hat_genetivattribut = soup.find(id=re.compile('.*-2-2$'))
    if hat_genetivattribut is not None:
        spans.extend(hat_genetivattribut.find_all('span', class_='wp-rel'))

    in_koordination_mit = soup.find(id=re.compile('.*-2-0$'))
    if in_koordination_mit is not None:
        spans.extend(in_koordination_mit.find_all('span', class_='wp-rel'))

    return [span.text.strip() for span in spans]

def get_assosications_from_duden(word):
    # nouns have to be capitalized!
    weird_url_stuff_dict = {
        'Ekel' : 'Ekel_Gefuehl_Abscheu',
        'ekel': 'Ekel_Gefuehl_Abscheu'
    }
    word = weird_url_stuff_dict[word] if word in weird_url_stuff_dict else convert_umlaute(capitalize(word))

    url = 'https://www.duden.de/rechtschreibung/' + word
    print(f'scraping {url}')

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    assosications = set()

    synonyms = soup.find(id='synonyme')
    if synonyms is not None:
        synonyms = synonyms.find('ul')
        assosications.update([
                synonym.text for synonym in synonyms.find_all('a')
            ])
    tag_cluster = soup.find('figure', class_='tag-cluster__cluster')
    if tag_cluster is not None:
        assosications.update([
                cluster.text for cluster in tag_cluster.find_all('a')
            ])
    return list(assosications)

def get_assosications_from_synonyme_de(word):
    # lower or upper case doesn't matter 
    word = convert_umlaute(capitalize(word))
    url = 'https://www.synonyme.de/' + word + '/'
    print(f'scraping {url}')

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    assosications = set()

    synonyms = soup.find_all('div', class_='synonymes')
    if synonyms is not None:
        for synonym in synonyms:
            a  = synonym.find('a')
            if a is not None:
                assosications.add(a.text.strip())
    return list(assosications)

def get_first_degree_assosiactions(dirpath, emotionlist):
    # Idea: get words and keep score of how often they are entered
    # words that appear more often are stronger related to the feeling they describe

    ressources = {
        'wordassosiaction': {
            'function': get_assosications_from_wordassociations,
            'reliability': 0.8
        },
        'dwds': {
            'function': get_assosications_from_dwds,
            'reliability': 0.5
        },
        'synonyme_de': {
            'function': get_assosications_from_synonyme_de,
            'reliability': 1.0
        },
        'duden': {
            'function': get_assosications_from_duden,
            'reliability': 1.0
        }
    }
    all_assosications = dict.fromkeys(emotionlist)

    for emotion in emotionlist:
        all_assosications[emotion] = {}
        print(f'=======================================================\n{emotion.upper()}\n\n')
        for ressource_value in ressources.values():
            new_assosiactions = ressource_value['function'](emotion)
            print(f'=> got {len(new_assosiactions)} new elements')
            for new_assosiaction in new_assosiactions:
                if new_assosiaction not in all_assosications[emotion]:
                    all_assosications[emotion][new_assosiaction] = ressource_value['reliability']
                else:
                    all_assosications[emotion][new_assosiaction] += ressource_value['reliability']
        add_to_csv(
            os.path.join(dirpath, emotion + '.txt'),
            all_assosications[emotion]
            )

def get_second_degree_assosiactions(dirpath, emotionlist):
    ressources = {
        'wordassosiaction': {
            'function': get_assosications_from_wordassociations,
            'reliability': 0.8
        },
        'synonyme_de': {
            'function': get_assosications_from_synonyme_de,
            'reliability': 1.0
        },
        'duden': {
            'function': get_assosications_from_duden,
            'reliability': 1.0
        }
    }
    all_assosications = dict([emotion, 
        load_csv_file(os.path.join(dirpath, emotion + '.txt'))]
        for emotion in emotionlist)

    for assosication in all_assosications:
        print(assosication, len(all_assosications[assosication]))

    for emotion in emotionlist:
            filepath = os.path.join(dirpath, emotion + '.txt')
            existing_assosications = dict([key, value]
                for key, value in all_assosications[emotion].items()
                if value > 1.0)
            print(f'=======================================================\n\
                        {emotion}\n')
            for assosication in existing_assosications:
                for ressource_name, ressource_value in ressources.items():
                    new_assosiactions = dict.fromkeys(ressource_value['function'](assosication),
                        ressource_value['reliability']/2)
                for new_assosiaction in new_assosiactions:
                    if new_assosiaction not in all_assosications[emotion]:
                        all_assosications[emotion][new_assosiaction] = ressource_value['reliability'] / 2
                    else:
                        all_assosications[emotion][new_assosiaction] += ressource_value['reliability'] / 2

            # save to txt files, duplicates are handled there
            add_to_csv(
                os.path.join(dirpath, emotion + '.txt'),
                dict([word, score]
                    for word, score in all_assosications[emotion].items()
                    if score > 0.5
                ))

# Not yet used:
def adding_words_using_comparison_on_dwds(reference, comparison):
    # expects refernce and comparison to be words and wordlist to be a list
    url = 'https://www.dwds.de/wp?q=' + reference + '&comp-method=diff&comp=' + comparison + '&pos=2&minstat=0&minfreq=5&by=logDice&limit=100&view=table'

    with webdriver.Firefox() as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 40)
        wait.until(presence_of_element_located((By.CSS_SELECTOR, "tr")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

    background_color_dict = {
        '#EFFAFF': reference,
        '#D9F1FF': reference,
        '#FFF0F0': comparison,
        '#ffe3e3': comparison
    }

    words_belonging_to = {
        reference: set(),
        comparison: set()
    }

    trs = soup.find_all('tr')
    if trs is not None:
        for tr in trs:
            found = tr.find('span', class_='wp-rel')
            if found is not None:
                found = found.text
                if count_words(found) == 1:
                    background_color = re.findall(r'#[0-9a-fA-F]{3,6}', tr['style'])[0]
                    if background_color in background_color_dict:
                        words_belonging_to[background_color_dict[background_color]].add(found)
    return words_belonging_to

def get_comparisions_from_dwds(dirpath, emotionlist):
    pass

