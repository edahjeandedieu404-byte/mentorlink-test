from .models import OffreMentorat

# Correspondance des niveaux pour calculer la proximité
NIVEAUX_ORDRE = {
    'L1': 1, 'L2': 2, 'L3': 3, 'M1': 4, 'M2': 5
}


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
        return 50  # neutre si non renseigné
    if filiere_mentor == filiere_mentore:
        return 100
    return 0


def calculer_score_niveau(niveau_mentor, niveau_mentore):
    """
    Plus les niveaux sont proches, plus le score est élevé.
    Le mentor doit être à un niveau supérieur ou égal au mentoré.
    """
    if not niveau_mentor or not niveau_mentore:
        return 50  # neutre si non renseigné

    ordre_mentor = NIVEAUX_ORDRE.get(niveau_mentor, 0)
    ordre_mentore = NIVEAUX_ORDRE.get(niveau_mentore, 0)

    if ordre_mentor == 0 or ordre_mentore == 0:
        return 50

    # Le mentor doit être à un niveau >= mentoré
    if ordre_mentor < ordre_mentore:
        return 0  # mentor moins avancé que le mentoré = pas pertinent

    difference = ordre_mentor - ordre_mentore

    if difference == 0:
        return 80  # même niveau = bon mais pas parfait
    elif difference == 1:
        return 100  # 1 niveau d'écart = parfait
    elif difference == 2:
        return 70  # 2 niveaux = acceptable
    else:
        return 40  # trop d'écart


def calculer_score_global(offre, demande):
    """
    Score global pondéré :
    - Matières : 50%
    - Filière   : 30%
    - Niveau    : 20%
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

    score_global = (
        score_matieres * 0.50 +
        score_filiere  * 0.30 +
        score_niveau   * 0.20
    )

    return {
        'score': round(score_global, 2),
        'score_matieres': score_matieres,
        'score_filiere': score_filiere,
        'score_niveau': score_niveau,
    }


def trouver_mentors(demande):
    """
    Trouve les mentors compatibles pour une demande donnée.
    Exclut le mentoré lui-même et les relations déjà existantes.
    Retourne les résultats triés par score décroissant.
    """
    from .models import RelationMentorat

    # Récupérer les mentors déjà associés à ce mentoré
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

    resultats = []
    mentors_vus = {}

    for offre in offres:
        scores = calculer_score_global(offre, demande)

        # Ne garder que les résultats avec un score > 0
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
                }

    resultats = sorted(
        mentors_vus.values(),
        key=lambda x: x['score'],
        reverse=True
    )

    return resultats