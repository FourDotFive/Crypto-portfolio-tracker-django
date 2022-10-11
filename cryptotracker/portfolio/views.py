from .utils.cryptocompare_connection import *
from .utils.yfinance_connection import *
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.INFO, "Registration successful.")
            return redirect("main")
        messages.add_message(request, messages.ERROR, "Unsuccessful registration. Invalid information.")
    form = RegistrationForm()
    return render(request, "registration.html", context={"registration_form": form})


def main_page_view(request):
    messages.add_message(request, messages.INFO, "1")
    messages.add_message(request, messages.ERROR, "2")
    messages.add_message(request, messages.WARNING, "3")
    messages.add_message(request, messages.SUCCESS, "4")
    toplist_by_market_cap = get_toplist_by_market_cap(limit=10)
    context = {
        'toplist_by_market_cap': toplist_by_market_cap
    }
    return render(request, 'main.html', context=context)


def error_404_view(request, exception):
    return render(request, '404.html')


def crypto_graph_view(request, crypto):
    crypto_1y_data_dict = get_crypto_1y_data(crypto)
    context = {
        "crypto_usd": crypto.upper() + '-USD',
        "crypto_1y_data_dict": crypto_1y_data_dict
    }
    return render(request, 'crypto_chart.html', context=context)
