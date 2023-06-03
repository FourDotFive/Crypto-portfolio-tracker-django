from django.urls import path
from .views import *

urlpatterns = [
    path('registration', registration_view, name='registration'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('change_currency/<str:currency>', change_user_currency, name='change_currency')
]
