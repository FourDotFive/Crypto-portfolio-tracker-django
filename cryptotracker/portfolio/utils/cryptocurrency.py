import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pprint
import environ


env = environ.Env()
environ.Env.read_env()
cryptocompare_api_key = env('cryptocompare_api_key')


def get_toplist_by_market_cap(limit: int = 10):
    url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit={limit}&tsym=USD&api_key='
    try:
        response = requests.get(url + cryptocompare_api_key)
        data = json.loads(response.text)
        cleaned_data = {}
        for crypto in data['Data']:
            full_name = crypto['CoinInfo']['FullName']
            cleaned_data[full_name] = {
                'Symbol': crypto['CoinInfo']['Name'],
                'ImageUrl': 'https://www.cryptocompare.com' + crypto['CoinInfo']['ImageUrl']
            }
        return cleaned_data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        pprint.pprint(e)
        return e

