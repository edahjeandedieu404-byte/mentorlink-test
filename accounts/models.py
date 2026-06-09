from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, nom, prenom, mot_de_passe=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, nom=nom, prenom=prenom, **extra_fields)
        user.set_password(mot_de_passe)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, prenom, mot_de_passe=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nom, prenom, mot_de_passe, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    FILIERES = [
    ('IA', 'Intelligence Artificielle'),
    ('IM', 'Internet et Multimédia'),
    ('GL', 'Génie Logiciel'),
    ('SE', 'Systèmes Embarqués et Internet des Objets'),
    ('SI', 'Sécurité Informatique'),
]
    NIVEAUX = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True)
    filiere = models.CharField(max_length=10, choices=FILIERES, blank=True)
    niveau = models.CharField(max_length=5, choices=NIVEAUX, blank=True)
    competences = models.TextField(blank=True, help_text="Matières maîtrisées, séparées par des virgules")
    lacunes = models.TextField(blank=True, help_text="Matières où tu as besoin d'aide, séparées par des virgules")
    disponibilites = models.TextField(blank=True, help_text="Ex: Lundi 14h-16h, Mercredi 10h-12h")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"