from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegistrationForm
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings


def registration_view(request):
    context = {}
    print(request.user.is_anonymous)
    if request.user.is_anonymous == False:
        return redirect('dashboard')

    elif request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('dashboard')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'register2.html', context)
