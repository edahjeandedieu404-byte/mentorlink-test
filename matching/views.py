from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DemandeMentorat, RelationMentorat, OffreMentorat, HistoriqueMatching
from .algorithme import trouver_mentors, calculer_score
from .forms import OffreMentoratForm, DemandeMentoratForm


@login_required
def dashboard(request):
    mes_offres = OffreMentorat.objects.filter(mentor=request.user, est_active=True)
    mes_demandes = DemandeMentorat.objects.filter(mentore=request.user)
    mes_mentors = RelationMentorat.objects.filter(mentore=request.user)
    mes_mentores = RelationMentorat.objects.filter(mentor=request.user)

    return render(request, 'matching/dashboard.html', {
        'mes_offres': mes_offres,
        'mes_demandes': mes_demandes,
        'mes_mentors': mes_mentors,
        'mes_mentores': mes_mentores,
    })


@login_required
def find_mentor(request, demande_id):
    demande = get_object_or_404(DemandeMentorat, id=demande_id, mentore=request.user)
    resultats = trouver_mentors(demande)
    return render(request, 'matching/find_mentor.html', {
        'demande': demande,
        'resultats': resultats
    })


@login_required
def my_mentors(request):
    relations = RelationMentorat.objects.filter(mentore=request.user)
    return render(request, 'matching/my_mentors.html', {
        'relations': relations
    })


@login_required
def my_mentees(request):
    relations = RelationMentorat.objects.filter(mentor=request.user)
    return render(request, 'matching/my_mentees.html', {
        'relations': relations
    })


@login_required
def matching_results(request):
    historiques = HistoriqueMatching.objects.all().order_by('-date_creation')
    return render(request, 'matching/matching_results.html', {
        'historiques': historiques
    })


@login_required
def accepter_match(request, demande_id, offre_id):
    demande = get_object_or_404(DemandeMentorat, id=demande_id, mentore=request.user)
    offre = get_object_or_404(OffreMentorat, id=offre_id)

    relation_existante = RelationMentorat.objects.filter(
        mentor=offre.mentor,
        mentore=demande.mentore
    ).exists()

    if not relation_existante:
        RelationMentorat.objects.create(
            mentor=offre.mentor,
            mentore=demande.mentore,
            statut='actif'
        )
        vrai_score = calculer_score(
            offre.competences,
            demande.competences_recherchees
        )
        HistoriqueMatching.objects.create(
            mentor=offre.mentor,
            mentore=demande.mentore,
            score=vrai_score
        )

    return redirect('my_mentors')


@login_required
def creer_offre(request):
    if request.method == 'POST':
        form = OffreMentoratForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.mentor = request.user
            offre.save()
            return redirect('dashboard')
    else:
        form = OffreMentoratForm()
    return render(request, 'matching/creer_offre.html', {'form': form})


@login_required
def creer_demande(request):
    if request.method == 'POST':
        form = DemandeMentoratForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.mentore = request.user
            demande.save()
            return redirect('dashboard')
    else:
        form = DemandeMentoratForm()
    return render(request, 'matching/creer_demande.html', {'form': form})