from django.contrib import admin
from .models import *

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id", "user1", "user2", "created_at"]

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["id", "chat", "sender", "message"]