from .models import Played
from bs4 import BeautifulSoup
import dateparser
import os
import requests
from datetime import datetime


HLTB_SA = 'https://howlongtobeat.com/'  # Scheme and Authority of URL
METACRITIC_SA = 'http://metacritic.com/'
METACRITIC_HEADERS = {'User-Agent': 'Mozilla/5.0'}
HLTB_HEADERS = {'User-Agent': 'Mozilla/5.0'}
DDG_SA = 'https://duckduckgo.com/'
DDG_HEADERS = {}


def hltb_scrapper(hltbGameUrl):
    request = requests.get(
        hltbGameUrl,
        headers=HLTB_HEADERS
    )
    if request.status_code >= 400:
        raise ScrapRequestException(
            '* The scrapper got a ' + str(request.status_code) + ' status code from HowLongToBeat'
        )

    game = {}
    soup = BeautifulSoup(request.text, 'html.parser')

    name = soup.find('div', class_='profile_header')
    game['name'] = name.text.strip() if name is not None else None

    cover_url = soup.select('div.game_image img')
    # This was the previous one used, when the Scheme and authority was in the URL
    # game['cover_url'] = cover_url[0].get('src') if cover_url != [] else None
    game['cover_url'] = None
    if (cover_url != []):
        url = cover_url[0].get('src')
        game['cover_url'] = os.path.join(HLTB_SA, url.lstrip(os.path.sep)) if HLTB_SA not in url else url

    game_length = soup.select('div.game_times li div')
    game['hltb_length'] = _parse_text_time_into_float(game_length[0].text) if game_length != [] else None

    # Howlongtobeat is doing changes in the synopsis
    # synopsis = soup.find('div', class_='profile_summary_more')
    # game['synopsis'] = _parse_synopsis(synopsis.text.strip()) if synopsis is not None else None

    return game


def metacritic_scrapper(metacriticUrl):
    request = requests.get(
        metacriticUrl,
        headers=METACRITIC_HEADERS
    )

    if request.status_code >= 400:
        raise ScrapRequestException(
            '* The scrapper got a ' + str(request.status_code) + ' status code from Metacritic'
        )

    game = {}
    soup = BeautifulSoup(request.text, 'html.parser')

    developer = soup.select('.summary_detail.developer .data')
    game['developer'] = developer[0].text.strip() if developer != [] else None

    genres = soup.find('li', class_='product_genre')
    game['genres'] = _parse_genres(genres.get_text()) if genres is not None else None

    release_date = soup.select('.summary_detail.release_data .data')
    game['release_date'] = None
    if release_date != []:
        game['release_date'] = dateparser.parse(release_date[0].text.strip()).strftime('%Y-%m-%d')

    metacritic_score = soup.select('div.metascore_w.xlarge > span')
    game['metacritic_score'] = metacritic_score[0].text.strip() if metacritic_score != [] else None

    metacritic_synopsis = soup.select('li.summary_detail.product_summary span.blurb_expanded')
    if not metacritic_synopsis:
        metacritic_synopsis = soup.select('li.summary_detail.product_summary > span.data')

    game['synopsis'] = metacritic_synopsis[0].text.strip() if metacritic_synopsis != [] else None

    return game


def get_menus_data(user_id):
    years_beaten = Played.objects.filter(beaten=True).select_related('game') \
                                 .filter(game__user_id=user_id).dates('stopped_playing_at', 'year')
    years_beaten = [date_.strftime('%Y') for date_ in years_beaten][::-1]  # Reverse

    years_tried = Played.objects.filter(beaten=False).select_related('game') \
                                .filter(game__user_id=user_id).dates('stopped_playing_at', 'year')
    years_tried = [date_.strftime('%Y') for date_ in years_tried][::-1]  # Reverse

    return {
        'years_beaten': years_beaten,
        'years_tried': years_tried,
    }


def get_games_order(year):
    if not year:
        order = ['-game__order', '-created_at']
    else:
        order = ['-stopped_playing_at', '-created_at']
    return order


def get_meta_for_list_playeds(user_first_name, playeds, year=None, beaten=None):
    title = 'What is ' + user_first_name + ' playing?'
    description = None

    if len(playeds) > 2 and not year:  # Currently playing
        description = user_first_name + ' is playing ' + playeds[0].game.name + ', ' \
            + playeds[1].game.name + ', ' + playeds[2].game.name + ' and more!'

    else:
        if str(datetime.now().year) == year and beaten:
            title = user_first_name + ' did beat ' + str(len(playeds)) + ' games this year already!'

        elif year and beaten:  # Beaten games in a given year
            title = user_first_name + '\'s beaten games in ' + year + ': ' + str(len(playeds)) + ' games!'

        elif year:  # Tried games in a given year
            title = user_first_name + '\'s tried games in ' + year + '!'

        if len(playeds) > 2:
            description = 'Beaten ' + playeds[0].game.name + ', ' \
                + playeds[1].game.name + ', ' + playeds[2].game.name + ' and more!'

    return (title, description)


def get_meta_for_game_details(user_first_name, game):
    title = None
    description = None

    playeds = game.played_set.all()

    playeds_beaten = [played for played in playeds if played.beaten]
    playeds_tried = [played for played in playeds if played.stopped_playing_at and not played.beaten]
    played_playing = next((played for played in playeds if played.stopped_playing_at is None), None)

    if played_playing:
        title = user_first_name + ' is playing ' + played_playing.game.name
        description = played_playing.game.name + ' of ' + played_playing.game.developer + ', ' + user_first_name \
            + ' is beating it at the moment.'

    elif playeds_beaten:
        title = user_first_name + ' did beat ' + game.name + ' on ' + str(playeds_beaten[-1].stopped_playing_at.year)
        description = game.name + ' of ' + game.developer

    elif playeds_tried:
        title = user_first_name + ' tried ' + game.name + ' on ' + str(playeds_tried[-1].stopped_playing_at.year)
        description = game.name + ' of ' + game.developer

    return (title, description)


def _parse_genres(genres):
    return ' '.join(genres.split()).replace('Genre(s): ', '').strip()


def _parse_text_time_into_float(textTime):
    if '-' in textTime:
        textTime = textTime.split('-')[1]
    if 'Hours' in textTime:
        textTime = float(textTime.replace('Hours', '').replace('½', '.5').strip())
    elif 'Mins' in textTime:
        textTime = float(textTime.replace('Mins', '').strip()) / 60 // 0.01 / 100  # To hours, with 2 decimal places
    return textTime


def _parse_synopsis(synopsis):
    return synopsis.replace('...Read More', '')


class ScrapRequestException(Exception):
    pass
