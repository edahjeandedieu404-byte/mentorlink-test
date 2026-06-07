from django.contrib import admin
from .models import OffreMentorat, DemandeMentorat, RelationMentorat, HistoriqueMatching


@admin.register(OffreMentorat)
class OffreMentoratAdmin(admin.ModelAdmin):
    list_display = ['titre', 'mentor', 'est_active', 'date_creation']
    list_filter = ['est_active']
    search_fields = ['titre', 'competences']


@admin.register(DemandeMentorat)
class DemandeMentoratAdmin(admin.ModelAdmin):
    list_display = ['titre', 'mentore', 'date_creation']
    search_fields = ['titre', 'competences_recherchees']


@admin.register(RelationMentorat)
class RelationMentoratAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'mentore', 'statut', 'date_debut']
    list_filter = ['statut']


@admin.register(HistoriqueMatching)
class HistoriqueMatchingAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'mentore', 'score', 'date_creation']
    ordering = ['-date_creation']