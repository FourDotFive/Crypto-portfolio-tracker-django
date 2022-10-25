import pandas as pd

from ..models import Purchase, Sale
from .cryptocompare_connection import get_coins_prices_and_images


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


# Returns list of unique assets in the purchases or sales
def get_assets(queryset):
    assets = list(set([purchase['crypto'] for purchase in queryset]))
    return assets


def get_purchases_df(purchases):
    df = pd.DataFrame(list(purchases.values('crypto', 'date', 'price', 'amount')))
    df['spent'] = df['amount'] * df['price']
    return df


def clean_purchases_df(df):
    crypto_assets = list(set(df['crypto'].to_list()))
    market_prices, coin_images = get_coins_prices_and_images(','.join(crypto_assets))

    aggregation_functions = {
        'amount': 'sum',
        'spent': 'sum'
    }
    df = df.groupby(df['crypto']).aggregate(aggregation_functions)
    df = df.reset_index(drop=False)
    df['market_price'] = df['crypto'].map(market_prices)
    df['image'] = df['crypto'].map(coin_images)
    df = df.set_index('crypto')
    return df


def get_sales_df(sales):
    df = pd.DataFrame(list(sales.values('crypto', 'date', 'price', 'amount')))
    df['earned'] = df['amount'] * df['price']
    return df


def clean_sales_df(df):
    aggregation_functions = {
        'amount': 'sum',
        'earned': 'sum'
    }
    df = df.groupby(df['crypto']).aggregate(aggregation_functions)
    df = df.reset_index(drop=False)
    df = df.set_index('crypto')
    return df


def get_portfolio_df(request):
    user = request.user
    purchases = Purchase.objects.filter(user=user).values()
    if purchases:
        purchases_df = get_purchases_df(purchases)
        purchases_df = clean_purchases_df(purchases_df)

        # If there are some purchases
        sales = Sale.objects.filter(user=user).values()
        if sales:
            sales_df = get_sales_df(sales)
            sales_df = clean_sales_df(sales_df)

            portfolio_df = clean_portfolio_df(purchases_df, sales_df)
        else:
            portfolio_df = clean_portfolio_df(purchases_df)
    else:
        portfolio_df = pd.DataFrame({'': []})
    return portfolio_df


def clean_portfolio_df(purchases_df, sales_df=None):
    if sales_df is None:
        purchases_df['earned'] = 0
    else:
        sales_df = sales_df.reindex(purchases_df.index, fill_value=0)
        purchases_df['amount'] = purchases_df['amount'] - sales_df['amount']

        purchases_df['earned'] = round(sales_df['earned'], 2)
        purchases_df['earned'] = purchases_df['earned'].fillna(0)

    purchases_df['current_value'] = round(purchases_df['amount'] * purchases_df['market_price'], 2)
    purchases_df['average_price'] = (purchases_df['spent'] - purchases_df['earned']) / purchases_df['amount']
    purchases_df.loc[purchases_df['average_price'] < 0, 'average_price'] = 0
    purchases_df['total_profit'] = round(purchases_df['earned'] - purchases_df['spent'] + purchases_df['current_value'], 2)

    return purchases_df


def get_available_assets_and_amount(request) -> dict:
    portfolio_df = get_portfolio_df(request)
    portfolio_df.drop(['spent', 'average_price', 'market_price'], axis=1, inplace=True)
    return portfolio_df['amount'].to_dict()


def get_list_for_choices(assets: dict) -> list:
    return [(k, k) for (k, v) in assets.items()]


def get_portfolio_dict(portfolio_df) -> dict:
    portfolio = portfolio_df.to_dict('index')

    for crypto, data in portfolio.items():
        amount = portfolio[crypto]['amount']
        average_price = portfolio[crypto]['average_price']
        portfolio[crypto]['amount'] = round(amount, get_n_for_rounding(amount) + 1)
        portfolio[crypto]['average_price'] = round(average_price, get_n_for_rounding(average_price) + 1)

    return portfolio

