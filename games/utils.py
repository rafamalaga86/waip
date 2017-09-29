import requests
import os
import time
from bs4 import BeautifulSoup


HLTB_SA = 'https://howlongtobeat.com/'  # Scheme and Authority of URL
METACRITIC_SA = 'http://metacritic.com/'
METACRITIC_HEADERS = {'User-Agent': 'Mozilla/5.0'}
HLTB_HEADERS = {}
DDG_SA = 'https://duckduckgo.com/'
DDG_HEADERS = {}


def hltb_scrapper(hltbGameUrl):
        request = requests.get(
            hltbGameUrl,
            headers=HLTB_HEADERS
        )

        game = {}
        soup = BeautifulSoup(request.text, 'html.parser')

        game['name'] = soup.find('div', class_='profile_header').text.strip()
        game['coverUrl'] = os.path.join(
            HLTB_SA,
            soup.find('div', class_='game_image').find('img').get('src')
        )
        gameTimes = soup.find('div', class_='game_times').findAll('li')
        game['hltbLength'] = gameTimes[0].find('div').text.strip()
        game['synopsis'] = soup.find('div', class_='profile_header_alt').text.strip()

        return game


def metacritic_scrapper(metacriticUrl):
        request = requests.get(
            metacriticUrl,
            headers=METACRITIC_HEADERS
        )

        game = {}
        soup = BeautifulSoup(request.text, 'html.parser')

        # Metacritic Scrap
        game['developer'] = soup.find(class_='summary_detail developer') \
            .find(class_='data').text.strip()

        game['genres'] = soup.find(class_='summary_detail product_genre') \
            .find(class_='data').text.strip()

        game['releaseDate'] = soup.find(class_='summary_detail release_data') \
            .find(class_='data').text.strip()

        game['metacriticScore'] = soup.select('div.metascore_w.xlarge > span')[0] \
            .text.strip()

        # game['metacriticUserScore'] = soup.select('div.metascore_w.user.large')[0] \
        #     .text.strip()

        return game


def ddg_scrapper(keywords):
    """
    Scraps firt page of Duck Duck Go with the given keywords

    :param str keywords: An integer or string

    :return: page titles as key and url as value
    :rtype: dict
    """
    tries = 3
    response_is_not_403 = False

    # Often Duck Duck Go sends 403 after sending the same keywords for 3 times
    # This loops prevents that changing the order of the keyword each time
    params = {
        'q': keywords,
        's': '1',
    }

    while tries > 0 or response_is_not_403:
        ddg_request = requests.post(
            DDG_SA + 'html/',
            data=params,
        )
        if ddg_request.status_code == 403:
            tries -= 1
            params['q'] = _reorderString(params['q'])
            time.sleep(15)
        else:
            response_is_not_403 = True

    if ddg_request.status_code != 200:
        raise Exception(
            'Status code: ' +
            str(ddg_request.status_code) +
            '\nMessage: ' +
            ddg_request.text
        )

    duck_duck_go_soup = BeautifulSoup(ddg_request.text, 'html.parser')

    div_block_list = duck_duck_go_soup.find_all('div', class_='results_links')

    raise Exception(div_block_list)

    titles = list(map(lambda x: x.find('a').get('href'), div_block_list))
    urls = list(map(lambda x: x.find('a').get('href'), div_block_list))

    return dict(zip(titles, urls))


def _reorderString(string):
    words = string.split(' ')
    words = words[-1:] + words[:-1]
    return ' '.join(words)
