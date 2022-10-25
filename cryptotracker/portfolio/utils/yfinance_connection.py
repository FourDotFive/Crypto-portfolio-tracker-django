import yfinance as yf
from .portfolio_utils import get_n_for_rounding


def get_crypto_graph_data(cryptocurrency: str):
    cryptocurrency = cryptocurrency.upper() + '-USD'
    ticker = yf.Ticker(cryptocurrency)
    crypto_data = ticker.history(period="2y")
    crypto_data.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1, inplace=True)
    n = get_n_for_rounding(crypto_data.iloc[0, 0])
    crypto_data = crypto_data.round(n)
    # Change index column format from datetime to str to return a json as context
    crypto_data.index = crypto_data.index.strftime('%Y-%m-%d')
    crypto_data.reset_index(inplace=True)
    crypto_data = crypto_data.values.tolist()
    return crypto_data
