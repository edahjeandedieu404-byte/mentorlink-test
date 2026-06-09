from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.inscription, name='inscription'),
    path('login/', views.connexion, name='connexion'),
    path('logout/', views.deconnexion, name='deconnexion'),
    path('profile/', views.profil, name='profil'),
    path('edit-profile/', views.modifier_profil, name='modifier_profil'),
]