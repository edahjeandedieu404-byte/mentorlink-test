from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ['email', 'nom', 'prenom', 'filiere', 'niveau', 'date_inscription']
    list_filter = ['filiere', 'niveau', 'is_active']
    search_fields = ['email', 'nom', 'prenom', 'telephone']
    ordering = ['-date_inscription']

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('email', 'nom', 'prenom', 'telephone', 'photo')
        }),
        ('Académique', {
            'fields': ('filiere', 'niveau', 'competences', 'lacunes', 'disponibilites', 'bio')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        ('Créer un utilisateur', {
            'fields': ('email', 'nom', 'prenom', 'telephone', 'password1', 'password2')
        }),
    )