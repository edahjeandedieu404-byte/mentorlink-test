from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'date_creation']
    ordering = ['-date_creation']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['auteur', 'conversation', 'contenu', 'date_envoi', 'lu']
    list_filter = ['lu']
    search_fields = ['contenu', 'auteur__email']
    ordering = ['-date_envoi']