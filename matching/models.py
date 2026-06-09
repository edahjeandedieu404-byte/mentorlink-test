from django.db import models
from django.conf import settings


class Matiere(models.Model):
    CATEGORIES = [
    ('info', 'Informatique générale'),
    ('math', 'Mathématiques'),
    ('reseau', 'Réseaux'),
    ('bd', 'Bases de données'),
    ('dev', 'Développement'),
    ('ia', 'Intelligence Artificielle'),
    ('securite', 'Sécurité'),
    ('autre', 'Autre'),
]
    nom = models.CharField(max_length=100, unique=True)
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='autre')

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']


class OffreMentorat(models.Model):
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offres_mentorat"
    )
    titre = models.CharField(max_length=200)
    description = models.TextField()
    matieres = models.ManyToManyField(Matiere, blank=True, related_name='offres')
    competences = models.TextField(
        blank=True,
        help_text="Compétences supplémentaires"
    )
    est_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class DemandeMentorat(models.Model):
    mentore = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="demandes_mentorat"
    )
    titre = models.CharField(max_length=200)
    objectif = models.TextField()
    matieres = models.ManyToManyField(Matiere, blank=True, related_name='demandes')
    competences_recherchees = models.TextField(
        blank=True,
        help_text="Compétences supplémentaires recherchées"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class RelationMentorat(models.Model):
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="relations_mentor"
    )
    mentore = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="relations_mentore"
    )
    statut = models.CharField(max_length=20, default="actif")
    date_debut = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mentor} → {self.mentore}"


class HistoriqueMatching(models.Model):
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="historique_en_tant_que_mentor"
    )
    mentore = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="historique_en_tant_que_mentore"
    )
    score = models.FloatField()
    score_matieres = models.FloatField(default=0)
    score_filiere = models.FloatField(default=0)
    score_niveau = models.FloatField(default=0)
    score_dispos = models.FloatField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mentor} ↔ {self.mentore} ({self.score}%)"