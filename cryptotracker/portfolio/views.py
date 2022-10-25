import json

from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginForm, PurchaseForm, SaleForm
from .models import Purchase, Sale
from .utils.cryptocompare_connection import get_toplist_by_market_cap
from .utils.portfolio_utils import get_available_assets_and_amount, get_portfolio_df, get_portfolio_dict
from .utils.yfinance_connection import get_crypto_graph_data


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                f'Welcome {user.username}',
                extra_tags='Successful registration'
            )
            return redirect('main')
        messages.add_message(
            request,
            messages.WARNING, 'Follow the instructions.',
            extra_tags='Unsuccessful registration'
        )
        return render(request, 'registration.html', context={'registration_form': form})

    form = RegistrationForm()
    return render(request, 'registration.html', context={'registration_form': form})


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f'You are now logged in as {username}.',
                    extra_tags='Welcome back'
                )
                return redirect('main')
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    'Invalid username or password.',
                    extra_tags='Unsuccessful login'
                )
                return render(request, 'login.html', context={'login_form': form})
    form = LoginForm()
    return render(request, 'login.html', context={'login_form': form})


@login_required(login_url='/login')
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('main')


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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def delete_portfolio_view(request):
    user = request.user
    Purchase.objects.filter(user=user).delete()
    Sale.objects.filter(user=user).delete()
    context = {
        # 'portfolio': portfolio
    }
    return render(request, 'portfolio.html', context=context)


def crypto_graph_view(request, crypto):
    crypto_data_dict = get_crypto_graph_data(crypto)
    context = {
        "crypto_usd": crypto.upper() + '-USD',
        "crypto_data_dict": crypto_data_dict
    }
    return render(request, 'crypto_chart.html', context=context)



