from .models import Game
from bs4 import BeautifulSoup
from datetime import date
import dateparser
import os
import requests


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
        if request.status_code >= 400:
            raise Exception('* The scrapper got a ' + str(request.status_code) + ' status code from HowLongToBeat')

        game = {}
        soup = BeautifulSoup(request.text, 'html.parser')

        name = soup.find('div', class_='profile_header')
        game['name'] = name.text.strip() if name is not None else None

        cover_url = soup.select('div.game_image img')
        game['cover_url'] = os.path.join(HLTB_SA, cover_url[0].get('src')) if cover_url != [] else None

        game_length = soup.select('div.game_times li div')
        game['hltb_length'] = _parse_text_time_into_float(game_length[0].text) if game_length != [] else None

        synopsis = soup.find('div', class_='profile_header_alt')
        game['synopsis'] = _parse_synopsis(synopsis.text.strip()) if synopsis is not None else None

        return game


def metacritic_scrapper(metacriticUrl):
        request = requests.get(
            metacriticUrl,
            headers=METACRITIC_HEADERS
        )

        if request.status_code >= 400:
            raise Exception('* The scrapper got a ' + str(request.status_code) + ' status code from Metacritic')

        game = {}
        soup = BeautifulSoup(request.text, 'html.parser')

        developer = soup.select('.summary_detail.developer .data')
        game['developer'] = developer[0].text.strip() if developer != [] else None

        genres = soup.select('.summary_detail.product_genre .data')
        game['genres'] = _parse_genres(genres[0].text.strip()) if genres != [] else None

        release_date = soup.select('.summary_detail.release_data .data')
        game['release_date'] = dateparser.parse(release_date[0].text.strip()).strftime('%Y-%m-%d') if release_date != [] else None

        metacritic_score = soup.select('div.metascore_w.xlarge > span')
        game['metacritic_score'] = metacritic_score[0].text.strip() if metacritic_score != [] else None

        return game


def get_menus_data(user_id):
    years_beaten = Game.objects.filter(user_id=user_id, beaten=True)\
        .dates('stopped_playing_at', 'year')
    years_beaten = [date.strftime('%Y') for date in years_beaten][::-1]  # Reverse
    today = date.today().strftime('%Y')
    if today in years_beaten:
        years_beaten.remove(today)

    years_played = Game.objects.filter(user_id=user_id, beaten=False).dates('stopped_playing_at', 'year')
    years_played = ([date.strftime('%Y') for date in years_played])[::-1]  # Reverse
    if today in years_played:
        years_played.remove(today)

    return {
        'years_beaten': years_beaten,
        'years_played': years_played,
    }


def _parse_genres(genres):
    return genres.replace(' +', ', ')


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
