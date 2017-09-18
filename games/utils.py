import requests
import os
from bs4 import BeautifulSoup
from pprint import pprint


class GameScrapper():
    # Class Constants
    HLTB_SA = 'https://howlongtobeat.com/'  # Scheme and Authority of URL

    # Class Properties
    hltbRequest = None
    metacriticRequest = None

    # Class Methods
    def __init__(self, metacriticUrl, hltbUrl):
        self.metacriticRequest = requests.get(metacriticUrl, headers={'User-Agent': 'Mozilla/5.0'})
        self.hltbRequest = requests.get(hltbUrl)
        # TODO handle scrapping errors

    def getGame(self):
        # TODO check if initialise dictionaries
        game = {}

        metacriticSoup = BeautifulSoup(self.metacriticRequest.text, 'html.parser')
        hltbSoup = BeautifulSoup(self.hltbRequest.text, 'html.parser')

        # HLTB Scrap
        game['name'] = hltbSoup.find('div', class_='profile_header').text.strip()

        game['coverUrl'] = os.path.join(
            self.HLTB_SA,
            hltbSoup.find('div', class_='game_image').find('img').get('src')
        )

        gameTimes = hltbSoup.find('div', class_='game_times').findAll('li')
        game['hltbLength'] = gameTimes[0].find('div').text.strip()

        game['synopsis'] = hltbSoup.find('div', class_='profile_header_alt').text.strip()

        # Metacritic Scrap
        game['developer'] = metacriticSoup.find(class_='summary_detail developer') \
            .find(class_='data').text.strip()

        game['genres'] = metacriticSoup.find(class_='summary_detail product_genre') \
            .find(class_='data').text.strip()

        game['releaseDate'] = metacriticSoup.find(class_='summary_detail release_data') \
            .find(class_='data').text.strip()

        game['metacriticScore'] = metacriticSoup.select('div.metascore_w.xlarge > span')[0] \
            .text.strip()

        game['metacriticUserScore'] = metacriticSoup.select('div.metascore_w.user.large')[0] \
            .text.strip()

        return game


def getMetacriticScoreColour(score):
    try:
        score = int(score)
        if score >= 75:
            return '#6c3'
        elif score >= 50:
            return '#fc3'
        else:
            return '#f00'
    except ValueError:
        return '#6c3'


# ms = GameScrapper(
#     'http://www.metacritic.com/game/pc/pony-island',
#     'https://howlongtobeat.com/game.php?id=33405')

# ms.getData()

# pprint(vars(ms))

# except Exception as ex:
#     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#     message = template.format(type(ex).__name__, ex.args)
#     print(message)
