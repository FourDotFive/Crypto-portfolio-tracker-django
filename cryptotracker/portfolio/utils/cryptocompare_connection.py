import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import environ

env = environ.Env()
environ.Env.read_env()
cryptocompare_api_key = env('cryptocompare_api_key')


# https://min-api.cryptocompare.com/data/top/totalvolfull?limit=
# https://min-api.cryptocompare.com/data/top/mktcapfull?limit=
def get_toplist_by_market_cap(limit: int = 10):
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit={limit}&tsym=USD&api_key='
    try:
        response = requests.get(url + cryptocompare_api_key)
        data = json.loads(response.text)
        cleaned_data = {}
        for coin in data['Data']:
            full_name = coin['CoinInfo']['FullName']
            if full_name == 'Lunar':
                continue
            cleaned_data[full_name] = {
                'Symbol': coin['CoinInfo']['Name'],
                'ImageUrl': 'https://www.cryptocompare.com' + coin['CoinInfo']['ImageUrl']
            }
        return cleaned_data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def get_supported_coins():
    url = f'https://min-api.cryptocompare.com/data/all/coinlist?api_key='
    try:
        response = requests.get(url + cryptocompare_api_key)
        data = json.loads(response.text)
        data = data['Data']
        cleaned_data = {}
        for coin in data:
            try:
                cleaned_data[coin] = {
                    'Url': data[coin]['Url'],
                    'ImageUrl': data[coin]['ImageUrl'],
                    'Name': data[coin]['Name'],
                    'Symbol': data[coin]['Symbol'],
                    'CoinName': data[coin]['CoinName']
                }
            except KeyError:
                continue
        return cleaned_data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def get_coin_prices(coins: str, currency: str = 'USD'):
    url = f'https://min-api.cryptocompare.com/data/pricemulti?fsyms={coins.upper()}&tsyms={currency.upper()}&api_key='
    try:
        response = requests.get(url + cryptocompare_api_key)
        data = json.loads(response.text)
        prices = {k: v[currency] for (k, v) in data.items()}
        return prices
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def get_coins_prices_and_images(coins: str, currency: str = 'USD'):
    url = f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={coins.upper()}&tsyms={currency.upper()}&api_key='
    try:
        response = requests.get(url + cryptocompare_api_key)
        data = json.loads(response.text)
        prices = {}
        images = {}
        for coin in data['RAW']:
            prices[coin] = data['RAW'][coin][currency]['PRICE']
            images[coin] = 'https://www.cryptocompare.com' + data['RAW'][coin][currency]['IMAGEURL']
        return prices, images
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e
