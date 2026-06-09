# -*- coding: utf-8 -*-
from matching.models import Matiere

matieres = [
    'Python',
    'Algorithme',
    'Bases de Données',
    'SQL',
    'Développement Web',
    'HTML/CSS',
    'Java',
    'Mathématique',
    'Réseau',
    'Anglais',
    'Language C',
]

for nom in matieres:
    Matiere.objects.get_or_create(nom=nom)

print(f"{Matiere.objects.count()} matières en base.")