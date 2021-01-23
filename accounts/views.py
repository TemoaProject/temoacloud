from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.forms import RegistrationForm, AccountAuthenticationForm
from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, HttpResponseRedirect
from accounts.models import Account
from django.contrib import messages


def registration_view(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(data=request.POST)
        if registration_form.is_valid():
            registration_form.save()
            email = request.POST['email']
            password = request.POST['password1']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("project.index"))
    else:
        registration_form = RegistrationForm()
    return render(request, 'register.html', context={'registration_form': registration_form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def user_login(request):
    context = {}
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("project.index"))
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form

    return render(request, "login.html", context)


