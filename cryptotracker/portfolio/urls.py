from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page_view, name='main'),
    path('graph/<str:crypto>', crypto_history_graph_view, name='graph'),
    path('cryptocurrencies', cryptocurrencies_view, name='cryptocurrencies'),
    path('portfolio', portfolio_view, name='portfolio'),
    path('new_purchase', new_purchase_view, name='new_purchase'),
    path('new_sale', new_sale_view, name='new_sale'),
    path('get_all_purchases', get_all_purchases_view, name='get_all_purchases'),
]
