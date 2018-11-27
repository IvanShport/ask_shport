from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from authorization.forms import LoginForm, RegForm, SettingsForm
from authorization.models import Profile

def LoginView(request):
    url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        url = request.POST.get('next', '/')
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(url)
    else:
        form = LoginForm()
    return render(request, 'authorization/login.html', {
        'form': form,
        'next': url
        })

def LogoutView(request):
    logout(request)
    url = request.GET.get('next', '/')
    return HttpResponseRedirect(url)


def RegistrationView(request):
    if request.method == 'POST':
        form = RegForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            url = request.POST.get('next', '/')
            return HttpResponseRedirect(url)
    else:
        form = RegForm()
    return render(request, 'authorization/registration.html', {'form': form })


@login_required
def SettingsView(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            url = request.POST.get('next', '/')
            return HttpResponseRedirect(url)
    else:
        prof = get_object_or_404(Profile, user = request.user)
        try:
            avatar = prof.avatar.url
        except ValueError:
            avatar = None
        form = SettingsForm(initial={'first_name' : request.user.first_name,
                'last_name' : request.user.last_name,
                'username' : request.user.username,
                'avatar': avatar})
    return render(request, 'authorization/settings.html', {'form': form})




