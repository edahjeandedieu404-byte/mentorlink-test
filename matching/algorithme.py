from .models import OffreMentorat


def calculer_score(competences_mentor, competences_mentore):
    if not competences_mentor or not competences_mentore:
        return 0

    set_mentor = set(c.strip().lower() for c in competences_mentor.split(','))
    set_mentore = set(c.strip().lower() for c in competences_mentore.split(','))

    if not set_mentore:
        return 0

    commun = set_mentor & set_mentore
    score = (len(commun) / len(set_mentore)) * 100
    return round(score, 2)


def trouver_mentors(demande):
    offres = OffreMentorat.objects.filter(est_active=True).exclude(
        mentor=demande.mentore
    )

    resultats = []
    mentors_vus = {}

    for offre in offres:
        score = calculer_score(
            offre.competences,
            demande.competences_recherchees
        )

        if score > 0:
            mentor_id = offre.mentor.id
            if mentor_id not in mentors_vus or score > mentors_vus[mentor_id]['score']:
                mentors_vus[mentor_id] = {
                    'mentor_id': mentor_id,
                    'mentor': offre.mentor,
                    'offre': offre,
                    'score': score
                }

    resultats = sorted(mentors_vus.values(), key=lambda x: x['score'], reverse=True)
    return resultats