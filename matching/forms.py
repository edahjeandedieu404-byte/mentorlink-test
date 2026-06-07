from django import forms
from .models import OffreMentorat, DemandeMentorat


class OffreMentoratForm(forms.ModelForm):
    class Meta:
        model = OffreMentorat
        fields = ['titre', 'description', 'competences']
        widgets = {
            'titre': forms.TextInput(attrs={
                'placeholder': 'Ex: Aide en Algorithmique et Python'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Décris ce que tu peux apporter...'
            }),
            'competences': forms.TextInput(attrs={
                'placeholder': 'Ex: Python, Algorithmique, BDD'
            }),
        }
        labels = {
            'titre': "Titre de l'offre",
            'description': 'Description',
            'competences': 'Compétences (séparées par des virgules)',
        }


class DemandeMentoratForm(forms.ModelForm):
    class Meta:
        model = DemandeMentorat
        fields = ['titre', 'objectif', 'competences_recherchees']
        widgets = {
            'titre': forms.TextInput(attrs={
                'placeholder': 'Ex: Besoin d\'aide en Python'
            }),
            'objectif': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Décris ce que tu veux apprendre...'
            }),
            'competences_recherchees': forms.TextInput(attrs={
                'placeholder': 'Ex: Python, Réseaux, SQL'
            }),
        }
        labels = {
            'titre': 'Titre de la demande',
            'objectif': 'Objectif',
            'competences_recherchees': 'Compétences recherchées (séparées par des virgules)',
        }