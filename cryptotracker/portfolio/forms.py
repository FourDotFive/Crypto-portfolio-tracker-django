import datetime
import json

from django import forms
from django.core.exceptions import ValidationError

from .models import Purchase, Sale
from .utils.portfolio_utils import get_list_for_choices


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
            raise ValidationError(f'Amount value should be less than {self.available_crypto_assets_and_amount[crypto]}')
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


