import requests
import os
from bs4 import BeautifulSoup
import dateparser
from .models import Game


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
        game['coverUrl'] = os.path.join(HLTB_SA, soup.find('div', class_='game_image').find('img').get('src'))
        gameTimes = soup.find('div', class_='game_times').findAll('li')
        gameTimeText = gameTimes[0].find('div').text
        game['hltbLength'] = _parse_text_time_into_float(gameTimeText)
        game['synopsis'] = _parse_synopsis(soup.find('div', class_='profile_header_alt').text.strip())

        return game


def metacritic_scrapper(metacriticUrl):
        request = requests.get(
            metacriticUrl,
            headers=METACRITIC_HEADERS
        )

        game = {}
        soup = BeautifulSoup(request.text, 'html.parser')

        # Metacritic Scrap
        game['developer'] = soup.find(class_='summary_detail developer').find(class_='data').text.strip()
        game['genres'] = soup.find(class_='summary_detail product_genre').find(class_='data').text.strip()
        game['releaseDate'] = dateparser.parse(
            soup.find(class_='summary_detail release_data').find(class_='data').text.strip()).strftime('%Y-%m-%d')
        game['metacriticScore'] = soup.select('div.metascore_w.xlarge > span')[0].text.strip()

        return game


def get_menus_data(user_id):
    years = Game.objects.filter(user_id=user_id).dates('stopped_playing_at', 'year')
    years = [date.strftime('%Y') for date in years]
    return {'years': years}


def _parse_text_time_into_float(textTime):
    if '-' in textTime:
        textTime = textTime.split('-')[1]
    if 'Hours' in textTime:
        result = float(textTime.replace('Hours', '').replace('½', '.5').strip())
    elif 'Mins' in textTime:
        result = float(textTime.replace('Mins', '').strip()) / 60 // 0.01 / 100  # To hours, with 2 decimal places
    return result


def _parse_synopsis(synopsis):
    return synopsis.replace('...Read More', '')
