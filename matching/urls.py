from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('creer-offre/', views.creer_offre, name='creer_offre'),
    path('creer-demande/', views.creer_demande, name='creer_demande'),
    path('find-mentor/<int:demande_id>/', views.find_mentor, name='find_mentor'),
    path('my-mentors/', views.my_mentors, name='my_mentors'),
    path('my-mentees/', views.my_mentees, name='my_mentees'),
    path('matching-results/', views.matching_results, name='matching_results'),
    path('accepter/<int:demande_id>/<int:offre_id>/', views.accepter_match, name='accepter_match'),
]