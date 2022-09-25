from django.shortcuts import render
from .utils.cryptocurrency import *


def main_page_view(request):
    data = get_toplist_by_market_cap(limit=10)
    return render(request, 'main_page.html')


def error_404_view(request, exception):
    return render(request, '404.html')
