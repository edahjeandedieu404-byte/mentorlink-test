from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm, ProfilForm


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Compte créé avec succès !")
            return redirect('dashboard')
        else:
            messages.error(request, "Erreur dans le formulaire. Vérifie les champs.")
    else:
        form = InscriptionForm()
    return render(request, 'accounts/inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenue {user.get_full_name()} !")
            return redirect('dashboard')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    else:
        form = ConnexionForm()
    return render(request, 'accounts/connexion.html', {'form': form})


@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('connexion')


@login_required
def profil(request):
    return render(request, 'accounts/profil.html', {'user': request.user})


@login_required
def modifier_profil(request):
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect('profil')
        else:
            messages.error(request, "Erreur dans le formulaire.")
    else:
        form = ProfilForm(instance=request.user)
    return render(request, 'accounts/modifier_profil.html', {'form': form})