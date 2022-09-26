from django.shortcuts import render
from .utils.cryptocurrency import *


def main_page_view(request):
    toplist_by_market_cap = get_toplist_by_market_cap(limit=30)
    context = {
        'toplist_by_market_cap': toplist_by_market_cap
    }
    return render(request, 'main_page.html', context=context)


def error_404_view(request, exception):
    return render(request, '404.html')
