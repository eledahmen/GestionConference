# UserApp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'participant'  # Rôle automatique
            user.save()
            messages.success(request, f"Compte créé ! Bienvenue, {user.username}.")
            return redirect('login')  # Redirigé vers login
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('conference_liste')  # Redirigé vers la page d'accueil