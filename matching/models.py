from django.db import models
from django.conf import settings


class OffreMentorat(models.Model):
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offres_mentorat"
    )
    titre = models.CharField(max_length=200)
    description = models.TextField()
    competences = models.TextField(
        help_text="Liste des compétences séparées par des virgules"
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
    competences_recherchees = models.TextField()
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
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mentor} ↔ {self.mentore} ({self.score}%)"