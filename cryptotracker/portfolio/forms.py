import datetime
import json

from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import Purchase, Sale
from .utils.portfolio_utils import get_list_for_choices


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username'
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )


class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.available_crypto_assets_and_amount = kwargs.pop('available_crypto_assets_and_amount', None)
        self.request = kwargs.pop('request', None)
        super(SaleForm, self).__init__(*args, **kwargs)
        if self.available_crypto_assets_and_amount is not None:
            assets_for_choices = get_list_for_choices(self.available_crypto_assets_and_amount)
            self.fields['crypto'].widget = forms.Select(choices=assets_for_choices)

    crypto = forms.CharField(
        label='Crypto Symbol',
        help_text='<ul><li>For example, BTC for Bitcoin or ETH for Ethereum.</li></ul>'
    )

    amount = forms.FloatField(
        help_text='<ul><li>Available amount of </li></ul>'
    )

    date = forms.DateField(
        label='Date When Sale Was Made',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )

    def clean_amount(self):
        crypto = self.cleaned_data.get('crypto')
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError('Amount value should greater than zero')
        if amount > self.available_crypto_assets_and_amount[crypto]:
            raise ValidationError(f'Amount value should less than {self.available_crypto_assets_and_amount[crypto]}')
        return amount

    class Meta:
        model = Sale
        fields = ['crypto', 'date', 'price', 'amount']


class PurchaseForm(forms.ModelForm):
    crypto = forms.CharField(
        label='Crypto Symbol',
        help_text='<ul><li>For example, BTC for Bitcoin or ETH for Ethereum.</li></ul>'
    )

    date = forms.DateField(
        label='Date When Purchase Was Made',
        widget=forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            )
    )

    def clean_crypto(self):
        crypto = self.cleaned_data.get('crypto')
        with open('all_coins.json') as json_file:
            all_coins = json.load(json_file)
        if crypto.upper() not in all_coins.keys():
            raise ValidationError('Unfortunately service does not support this coin')
        return crypto

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Price should greater than zero')
        return price

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError('Amount value should greater than zero')
        return amount

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date > datetime.date.today():
            raise ValidationError('Date should be less than or equal to system date')
        return date

    class Meta:
        model = Purchase
        fields = ['crypto', 'date', 'price', 'amount']


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        help_text='<ul><li>Minimum length is 5 characters, maximum is 32.</li>'
                  '<li>Can only contain letters, numbers, dashes and underscores.</li></ul>'
    )
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='<ul><li>Your password can’t be too similar to your other personal information.</li>'
                  '<li>Your password must contain at least 8 characters.</li></ul>'
    )

    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        help_text='Enter the same password as before, for verification.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 8:
            raise ValidationError('Nickname is too short')
        user = User.objects.filter(username=username)
        if user.count():
            raise ValidationError('User {} already exists'.format(username))
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('Passwords should have a minimum of 8 characters.')
        if len(password1) > 64:
            raise ValidationError('The maximum length of a password is 64 characters.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 != password1:
            raise ValidationError('The password and confirm password fields do not match')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user.count():
            raise ValidationError('User with such email already exists')
        return email
