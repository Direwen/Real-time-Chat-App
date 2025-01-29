from django.contrib.auth.models import User
from rest_framework import serializers
from core.serializers import UserSerializer
from .models import *

class ChatSerializer(serializers.ModelSerializer):
    
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)
    
    class Meta:
        model = Chat
        fields = ["id", "user1", "user2", "created_at"]
        
class CreateChatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def save(self, **kwargs):
        user_id = self.validated_data["user_id"]
        user = User.objects.get(pk=user_id)  # Get the user object by user_id
        current_user = self.context['request'].user  # Get the current user from the request context
        
        # Create the chat with both users (user and current_user)
        chat = Chat.objects.create(
            user1=user,
            user2=current_user
        )
        return chat

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "chat_id", "sender_id", "message", "created_at"]
        
    def save(self, **kwargs):
        message = self.validated_data["message"]
        user_sender = self.context["sender"]
        chat = Chat.objects.get(pk=self.context["chat_id"])
        #Create the chat message
        chat_message = ChatMessage.objects.create(
            chat=chat,
            sender=user_sender,
            message=message 
        )
        return chat_message