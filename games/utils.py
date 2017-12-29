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
