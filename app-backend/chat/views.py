from django.shortcuts import render
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from .models import *
from .serializers import *

from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Chat
from .serializers import ChatSerializer, CreateChatSerializer

class ChatViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    # Get queryset based on user (staff can view all chats, others only their own)
    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff:
            return Chat.objects.all()
        return Chat.objects.filter(Q(user1_id=current_user.id) | Q(user2_id=current_user.id))

    # Return the appropriate serializer based on the HTTP method
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateChatSerializer 
        return ChatSerializer

    # Optionally, you can pass additional context (e.g., current_user) if needed in your serializer
    def get_serializer_context(self):
        return {
            "current_user_id": self.request.user.id  # Pass only the user ID here (no need for whole user object)
        }

class ChatMessageViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatMessage.objects.filter(chat_id=self.kwargs["chat_pk"])
    
    def get_serializer_context(self):
        return {
            "chat_id" : self.kwargs["chat_pk"],
            "sender": self.request.user
        }
