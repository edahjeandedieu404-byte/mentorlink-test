import re
from .models import OffreMentorat

NIVEAUX_ORDRE = {
    'L1': 1, 'L2': 2, 'L3': 3, 'M1': 4, 'M2': 5
}

JOURS_SYNONYMES = {
    'lun': 'lundi', 'lundi': 'lundi',
    'mar': 'mardi', 'mardi': 'mardi',
    'mer': 'mercredi', 'mercredi': 'mercredi',
    'jeu': 'jeudi', 'jeudi': 'jeudi',
    'ven': 'vendredi', 'vendredi': 'vendredi',
    'sam': 'samedi', 'samedi': 'samedi',
    'dim': 'dimanche', 'dimanche': 'dimanche',
    'monday': 'lundi', 'tuesday': 'mardi', 'wednesday': 'mercredi',
    'thursday': 'jeudi', 'friday': 'vendredi', 'saturday': 'samedi',
    'sunday': 'dimanche',
}


def parser_disponibilites(texte):
    """
    Parse un texte de disponibilités et retourne une liste de créneaux.
    Ex: "Lundi 14h-16h, Mercredi 10h-12h" -> [('lundi', 14, 16), ('mercredi', 10, 12)]
    """
    if not texte:
        return []

    creneaux = []
    texte = texte.lower().strip()

    # Séparer par virgule ou point-virgule
    parties = re.split(r'[,;]', texte)

    for partie in parties:
        partie = partie.strip()

        # Chercher le jour
        jour_trouve = None
        for mot, jour in JOURS_SYNONYMES.items():
            if mot in partie:
                jour_trouve = jour
                break

        if not jour_trouve:
            continue

        # Chercher les heures (format: 14h, 14h30, 14:00, 14)
        heures = re.findall(r'(\d{1,2})(?:h|:)(\d{0,2})?', partie)

        if len(heures) >= 2:
            try:
                h_debut = int(heures[0][0])
                h_fin = int(heures[1][0])
                creneaux.append((jour_trouve, h_debut, h_fin))
            except (ValueError, IndexError):
                pass
        elif len(heures) == 1:
            try:
                h_debut = int(heures[0][0])
                creneaux.append((jour_trouve, h_debut, h_debut + 2))
            except (ValueError, IndexError):
                pass

    return creneaux


def chevauchement_heures(debut1, fin1, debut2, fin2):
    """Retourne le nombre d'heures de chevauchement entre deux créneaux."""
    debut_commun = max(debut1, debut2)
    fin_commun = min(fin1, fin2)
    return max(0, fin_commun - debut_commun)


def calculer_score_disponibilites(dispo_mentor, dispo_mentore):
    """
    Compare les disponibilités horaires entre mentor et mentoré.
    Retourne un score entre 0 et 100.
    """
    creneaux_mentor = parser_disponibilites(dispo_mentor)
    creneaux_mentore = parser_disponibilites(dispo_mentore)

    # Si l'un ou l'autre n'a pas renseigné ses dispos
    if not creneaux_mentor and not creneaux_mentore:
        return 50  # neutre
    if not creneaux_mentor or not creneaux_mentore:
        return 30  # pénalité légère si un seul a renseigné

    total_heures_mentore = sum(fin - debut for _, debut, fin in creneaux_mentore)
    if total_heures_mentore == 0:
        return 30

    heures_communes = 0
    for jour_m, debut_m, fin_m in creneaux_mentor:
        for jour_e, debut_e, fin_e in creneaux_mentore:
            if jour_m == jour_e:
                heures_communes += chevauchement_heures(debut_m, fin_m, debut_e, fin_e)

    score = min(100, (heures_communes / total_heures_mentore) * 100)
    return round(score, 2)


def calculer_score_matieres(matieres_mentor, matieres_mentore):
    """
    Compare les matières en commun entre mentor et mentoré.
    Retourne un score entre 0 et 100.
    """
    ids_mentor = set(matieres_mentor.values_list('id', flat=True))
    ids_mentore = set(matieres_mentore.values_list('id', flat=True))

    if not ids_mentore:
        return 0

    commun = ids_mentor & ids_mentore
    score = (len(commun) / len(ids_mentore)) * 100
    return round(score, 2)


def calculer_score_filiere(filiere_mentor, filiere_mentore):
    """
    Même filière = 100%, filières différentes = 0%.
    """
    if not filiere_mentor or not filiere_mentore:
        return 50
    if filiere_mentor == filiere_mentore:
        return 100
    return 0


def calculer_score_niveau(niveau_mentor, niveau_mentore):
    """
    Le mentor doit être à un niveau supérieur ou égal au mentoré.
    1 niveau d'écart = parfait, même niveau = bon, trop d'écart = moins bien.
    """
    if not niveau_mentor or not niveau_mentore:
        return 50

    ordre_mentor = NIVEAUX_ORDRE.get(niveau_mentor, 0)
    ordre_mentore = NIVEAUX_ORDRE.get(niveau_mentore, 0)

    if ordre_mentor == 0 or ordre_mentore == 0:
        return 50

    if ordre_mentor < ordre_mentore:
        return 0  # mentor moins avancé = pas pertinent

    difference = ordre_mentor - ordre_mentore

    if difference == 0:
        return 80
    elif difference == 1:
        return 100
    elif difference == 2:
        return 70
    else:
        return 40


def calculer_score_global(offre, demande):
    """
    Score global pondéré :
    - Matières       : 40%
    - Filière        : 25%
    - Niveau         : 15%
    - Disponibilités : 20%
    """
    score_matieres = calculer_score_matieres(
        offre.matieres.all(),
        demande.matieres.all()
    )
    score_filiere = calculer_score_filiere(
        offre.mentor.filiere,
        demande.mentore.filiere
    )
    score_niveau = calculer_score_niveau(
        offre.mentor.niveau,
        demande.mentore.niveau
    )
    score_dispos = calculer_score_disponibilites(
        offre.mentor.disponibilites,
        demande.mentore.disponibilites
    )

    score_global = (
        score_matieres * 0.40 +
        score_filiere  * 0.25 +
        score_niveau   * 0.15 +
        score_dispos   * 0.20
    )

    return {
        'score': round(score_global, 2),
        'score_matieres': score_matieres,
        'score_filiere': score_filiere,
        'score_niveau': score_niveau,
        'score_dispos': score_dispos,
    }


def trouver_mentors(demande):
    """
    Trouve les mentors compatibles pour une demande donnée.
    Exclut le mentoré lui-même et les relations déjà existantes.
    Retourne les résultats triés par score décroissant.
    """
    from .models import RelationMentorat

    mentors_existants = RelationMentorat.objects.filter(
        mentore=demande.mentore
    ).values_list('mentor_id', flat=True)

    offres = OffreMentorat.objects.filter(
        est_active=True
    ).exclude(
        mentor=demande.mentore
    ).exclude(
        mentor_id__in=mentors_existants
    ).select_related('mentor').prefetch_related('matieres')

    mentors_vus = {}

    for offre in offres:
        scores = calculer_score_global(offre, demande)

        if scores['score'] > 0:
            mentor_id = offre.mentor.id
            if mentor_id not in mentors_vus or scores['score'] > mentors_vus[mentor_id]['score']:
                mentors_vus[mentor_id] = {
                    'mentor_id': mentor_id,
                    'mentor': offre.mentor,
                    'offre': offre,
                    'score': scores['score'],
                    'score_matieres': scores['score_matieres'],
                    'score_filiere': scores['score_filiere'],
                    'score_niveau': scores['score_niveau'],
                    'score_dispos': scores['score_dispos'],
                }

    resultats = sorted(
        mentors_vus.values(),
        key=lambda x: x['score'],
        reverse=True
    )

    return resultats
