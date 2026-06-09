from django import forms
from .models import OffreMentorat, DemandeMentorat, Matiere


class OffreMentoratForm(forms.ModelForm):
    matieres = forms.ModelMultipleChoiceField(
        queryset=Matiere.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Matières que tu peux enseigner"
    )

    class Meta:
        model = OffreMentorat
        fields = ['titre', 'description', 'matieres', 'competences']
        widgets = {
            'titre': forms.TextInput(attrs={
                'placeholder': 'Ex: Aide en Algorithmique et Python',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Décris ce que tu peux apporter...',
                'class': 'form-control'
            }),
            'competences': forms.TextInput(attrs={
                'placeholder': 'Ex: Rigueur, Pédagogie (optionnel)',
                'class': 'form-control'
            }),
        }
        labels = {
            'titre': "Titre de l'offre",
            'description': 'Description',
            'competences': 'Compétences supplémentaires (optionnel)',
        }


class DemandeMentoratForm(forms.ModelForm):
    matieres = forms.ModelMultipleChoiceField(
        queryset=Matiere.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Matières où tu as besoin d'aide"
    )

    class Meta:
        model = DemandeMentorat
        fields = ['titre', 'objectif', 'matieres', 'competences_recherchees']
        widgets = {
            'titre': forms.TextInput(attrs={
                'placeholder': "Ex: Besoin d'aide en Python",
                'class': 'form-control'
            }),
            'objectif': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Décris ce que tu veux apprendre...',
                'class': 'form-control'
            }),
            'competences_recherchees': forms.TextInput(attrs={
                'placeholder': 'Ex: Patience, Disponibilité (optionnel)',
                'class': 'form-control'
            }),
        }
        labels = {
            'titre': 'Titre de la demande',
            'objectif': 'Objectif',
            'competences_recherchees': 'Qualités recherchées (optionnel)',
        }