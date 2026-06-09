from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Utilisateur


class InscriptionForm(forms.ModelForm):
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label="Mot de passe"
    )
    confirmer_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe'}),
        label="Confirmer le mot de passe"
    )

    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'telephone', 'filiere', 'niveau', 'competences', 'lacunes', 'disponibilites', 'bio', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'telephone': forms.TextInput(attrs={'placeholder': 'Numéro de téléphone'}),
            'competences': forms.TextInput(attrs={'placeholder': 'Ex: Python, Algorithmique, BDD'}),
            'lacunes': forms.TextInput(attrs={'placeholder': 'Ex: Réseaux, Mathématiques'}),
            'disponibilites': forms.TextInput(attrs={'placeholder': 'Ex: Lundi 14h-16h, Mercredi 10h-12h'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Parle de toi en quelques mots...', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mdp = cleaned_data.get("mot_de_passe")
        confirmation = cleaned_data.get("confirmer_mot_de_passe")
        if mdp and confirmation and mdp != confirmation:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["mot_de_passe"])
        if commit:
            user.save()
        return user


class ConnexionForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label="Mot de passe"
    )


class ProfilForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'telephone', 'filiere', 'niveau', 'competences', 'lacunes', 'disponibilites', 'bio', 'photo']
        widgets = {
            'competences': forms.TextInput(attrs={'placeholder': 'Ex: Python, Algorithmique'}),
            'lacunes': forms.TextInput(attrs={'placeholder': 'Ex: Réseaux, Maths'}),
            'disponibilites': forms.TextInput(attrs={'placeholder': 'Ex: Lundi 14h-16h'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }