from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page_view, name='main'),
    path('graph/<str:crypto>', crypto_graph_view, name='graph'),
    path('registration', registration_view, name='registration')
]
