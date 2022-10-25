from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page_view, name='main'),
    path('graph/<str:crypto>', crypto_graph_view, name='graph'),
    path('registration', registration_view, name='registration'),
    path('cryptocurrencies', cryptocurrencies_view, name='cryptocurrencies'),
    path('portfolio', portfolio_view, name='portfolio'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('delete_portfolio', delete_portfolio_view, name='delete_portfolio'),
    path('new_purchase', new_purchase_view, name='new_purchase'),
    path('new_sale', new_sale_view, name='new_sale'),
]
