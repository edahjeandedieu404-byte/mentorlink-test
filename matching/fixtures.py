# -*- coding: utf-8 -*-
from matching.models import Matiere

matieres = [
    'Algorithmique',
    'Langage C',
    'Bases de données relationnelles',
    'SQL',
    'Réseaux informatiques',
    'Programmation Java',
    'Mathématiques générales',
    'Mathématiques pour l\'Informatique',
    'Probabilités et Statistiques',
    'Anglais',
    'Systèmes d\'exploitation',
    'Programmation Web',
    'Structures de données',
    'Administration des systèmes',
]

for nom in matieres:
    Matiere.objects.get_or_create(nom=nom)

print(f"{Matiere.objects.count()} matières en base.")