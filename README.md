# MentorLink - Plateforme de mentorat étudiant

## Installation

### Prérequis
- Python 3.12+
- PostgreSQL 16
- Git

### Étapes

**1. Cloner le projet**

    git clone https://github.com/edahjeandedieu404-byte/PIL1_2526_31.git
    cd PIL1_2526_31

**2. Créer et activer l'environnement virtuel**

    python -m venv env
    env\Scripts\activate

**3. Installer les dépendances**

    pip install -r requirements.txt

**4. Créer la base de données PostgreSQL**

    psql -U postgres
    CREATE DATABASE mentorlink;
    \q

**5. Configurer settings.py**
Ouvrir mentorlink/settings.py et modifier PASSWORD avec ton mot de passe PostgreSQL.

**6. Appliquer les migrations**

    python manage.py migrate

**7. Insérer les matières**

    python manage.py shell

Puis copier-coller :

    exec(open('matching/fixtures.py', encoding='utf-8').read())
    exit()

**8. Créer un compte administrateur**

    python manage.py createsuperuser

**9. Lancer le serveur**

    python manage.py runserver

Accéder à : http://127.0.0.1:8000/