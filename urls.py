from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_conversations, name='liste_conversations'),
    path('conversation/<int:conversation_id>/', views.conversation, name='conversation'),
    path('nouvelle/<int:user_id>/', views.nouvelle_conversation, name='nouvelle_conversation'),
]