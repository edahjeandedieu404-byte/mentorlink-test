# Script pour ajouter les matières IFRI dans la base
# Lancer avec : python manage.py shell < matching/fixtures.py

from matching.models import Matiere

matieres = [
    # Informatique générale
    ('Algorithmique', 'info'),
    ('Structures de données', 'info'),
    ('Programmation Python', 'dev'),
    ('Programmation C/C++', 'dev'),
    ('Programmation Java', 'dev'),
    ('Développement Web', 'dev'),
    ('Développement Mobile', 'dev'),
    ('Git et versioning', 'dev'),

    # Bases de données
    ('Bases de données SQL', 'bd'),
    ('PostgreSQL', 'bd'),
    ('MySQL', 'bd'),
    ('MongoDB', 'bd'),
    ('Algèbre relationnelle', 'bd'),

    # Réseaux
    ('Réseaux informatiques', 'reseau'),
    ('Protocoles TCP/IP', 'reseau'),
    ('Administration système', 'reseau'),
    ('Linux/Unix', 'reseau'),

    # Intelligence Artificielle
    ('Machine Learning', 'ia'),
    ('Deep Learning', 'ia'),
    ('Traitement du langage naturel', 'ia'),
    ('Vision par ordinateur', 'ia'),
    ('Data Science', 'ia'),

    # Sécurité
    ('Cybersécurité', 'securite'),
    ('Cryptographie', 'securite'),
    ('Sécurité des réseaux', 'securite'),
    ('Ethical Hacking', 'securite'),

    # Mathématiques
    ('Mathématiques discrètes', 'math'),
    ('Probabilités et statistiques', 'math'),
    ('Algèbre linéaire', 'math'),
    ('Analyse mathématique', 'math'),
    ('Recherche opérationnelle', 'math'),

    # Autre
    ('Génie logiciel', 'autre'),
    ('UML et modélisation', 'autre'),
    ('Gestion de projet', 'autre'),
    ('Systèmes embarqués', 'autre'),
    ('Internet des objets (IoT)', 'autre'),
]

for nom, categorie in matieres:
    obj, created = Matiere.objects.get_or_create(
        nom=nom,
        defaults={'categorie': categorie}
    )
    if created:
        print(f"✓ Ajouté : {nom}")
    else:
        print(f"- Existe déjà : {nom}")

print("\nTerminé !")