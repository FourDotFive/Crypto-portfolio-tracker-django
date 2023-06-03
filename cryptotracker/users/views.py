from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegistrationForm, LoginForm
from .models import AppUser


@login_required(login_url='user/login')
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('main')


@login_required(login_url='user/login')
def change_user_currency(request, currency: str):
    available_currencies = ['USD', 'EUR', 'GBP']

    currency = currency.upper()
    if currency not in available_currencies:
        messages.add_message(
            request,
            messages.WARNING,
            'Unavailable currencies.',
            extra_tags='Unsuccessful change'
        )
        if request.META.get('HTTP_REFERER') is None:
            return redirect('main')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        AppUser.objects.filter(user=request.user).update(currency=currency)
        messages.add_message(
            request,
            messages.SUCCESS,
            f'All changes were applied.',
            extra_tags='Successful change'
        )
        if request.META.get('HTTP_REFERER') is None:
            return redirect('main')
    return redirect(request.META.get('HTTP_REFERER'))


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


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            AppUser.objects.create(user=user, currency='USD')
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