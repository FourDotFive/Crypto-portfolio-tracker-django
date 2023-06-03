import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PurchaseForm, SaleForm
from .models import Purchase, Sale
from .utils.cryptocompare_connection import get_toplist_by_market_cap, get_crypto_history
from .utils.portfolio_utils import get_available_assets_and_amount, get_portfolio_df, get_portfolio_dict, get_purchases_df


@login_required(login_url='user/login')
def new_purchase_view(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            crypto = form.cleaned_data.get('crypto').upper()
            date = form.cleaned_data.get('date')
            price = form.cleaned_data.get('price')
            amount = form.cleaned_data.get('amount')
            Purchase.objects.create(user=request.user, crypto=crypto, date=date, price=price, amount=amount)
            messages.add_message(
                request,
                messages.SUCCESS,
                f'Purchase Successfully registered.',
                extra_tags='New Purchase'
            )
            return redirect('portfolio')
        return render(request, 'new_purchase.html', context={'purchase_form': form})
    form = PurchaseForm()
    return render(request, 'new_purchase.html', context={'purchase_form': form})


@login_required(login_url='user/login')
def new_sale_view(request):
    available_crypto_assets_and_amount = get_available_assets_and_amount(request)
    if request.method == "POST":
        form = SaleForm(request.POST, available_crypto_assets_and_amount=available_crypto_assets_and_amount, request=request)
        if form.is_valid():
            crypto = form.cleaned_data.get('crypto').upper()
            date = form.cleaned_data.get('date')
            price = form.cleaned_data.get('price')
            amount = form.cleaned_data.get('amount')
            Sale.objects.create(user=request.user, crypto=crypto, date=date, price=price, amount=amount)
            messages.add_message(
                request,
                messages.SUCCESS,
                f'Purchase Sale registered.',
                extra_tags='New Sale'
            )
            return redirect('portfolio')
        context = {
            'sale_form': form,
            'available_crypto_assets_and_amount': json.dumps(available_crypto_assets_and_amount)
        }
        return render(request, 'new_sale.html', context=context)
    form = SaleForm(available_crypto_assets_and_amount=available_crypto_assets_and_amount, request=request)
    context = {
        'sale_form': form,
        'available_crypto_assets_and_amount': json.dumps(available_crypto_assets_and_amount)
    }
    return render(request, 'new_sale.html', context=context)


def main_page_view(request):
    return render(request, 'main.html', context={})


def cryptocurrencies_view(request):
    toplist_by_market_cap = get_toplist_by_market_cap(limit=13)
    context = {
        'toplist_by_market_cap': toplist_by_market_cap
    }
    return render(request, 'cryptocurrencies.html', context=context)


def error_404_view(request, exception):
    return render(request, '404.html')


@login_required(login_url='user/login')
def portfolio_view(request):
    portfolio_df = get_portfolio_df(request)

    if not portfolio_df.empty:
        portfolio = get_portfolio_dict(portfolio_df)
        data_for_pie = portfolio_df['current_value'].to_dict()
    else:
        portfolio = {}
        data_for_pie = {}

    context = {
        'portfolio': portfolio,
        'data_for_pie_graph': json.dumps(
            {
                'labels': list(data_for_pie.keys()),
                'values': list(data_for_pie.values()),
            }
        )
    }
    return render(request, 'portfolio.html', context=context)


def crypto_history_graph_view(request, crypto):
    crypto_history = get_crypto_history(crypto)
    context = {
        "crypto_usd": crypto.upper() + '-USD',
        "crypto_history": json.dumps(crypto_history)
    }
    return render(request, 'crypto_chart.html', context=context)


@login_required(login_url='user/login')
def get_all_purchases_view(request):
    purchases = Purchase.objects.filter(user=request.user).values()
    purchases_df = get_purchases_df(purchases)
    purchases_df.sort_values(by=['date'], inplace=True, ascending=False)

    purchases = purchases_df.to_dict('index')

    context = {
        'purchases': purchases
    }
    return render(request, 'all_purchases.html', context=context)
