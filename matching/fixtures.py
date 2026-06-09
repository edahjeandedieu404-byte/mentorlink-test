# -*- coding: utf-8 -*-
from matching.models import Matiere

matieres = [
    ('Python', 'dev'),
    ('Algorithme', 'info'),
    ('Bases de Données', 'bd'),
    ('SQL', 'bd'),
    ('Développement Web', 'dev'),
    ('HTML/CSS', 'dev'),
    ('Java', 'dev'),
    ('Mathématique', 'math'),
    ('Réseau', 'reseau'),
    ('Anglais', 'autre'),
    ('Language C', 'dev'),
]

for nom, cat in matieres:
    Matiere.objects.get_or_create(nom=nom, defaults={'categorie': cat})

print(f"{Matiere.objects.count()} matières en base.")