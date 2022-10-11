import yfinance as yf


def get_crypto_1y_data(cryptocurrency: str):
    cryptocurrency = cryptocurrency.upper() + '-USD'
    ticker = yf.Ticker(cryptocurrency)
    crypto_1y_data = ticker.history(period="800d")
    crypto_1y_data.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1, inplace=True)
    n = get_n_for_rounding(crypto_1y_data.iloc[0, 0])
    crypto_1y_data = crypto_1y_data.round(n)
    # Change index column format from datetime to str to return a json as context
    crypto_1y_data.index = crypto_1y_data.index.strftime('%Y-%m-%d')
    crypto_1y_data.reset_index(inplace=True)
    crypto_1y_data = crypto_1y_data.values.tolist()
    return crypto_1y_data


def get_n_for_rounding(value):
    if value >= 100:
        return 1
    elif value >= 10:
        return 2
    elif value >= 1:
        return 3
    elif value >= 0.1:
        return 4
    elif value >= 0.01:
        return 5
    else:
        return 8
