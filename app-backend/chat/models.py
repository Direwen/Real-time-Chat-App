from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Chat(models.Model):
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chats_as_user1'
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chats_as_user2'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user1} & {self.user2}"

    #APPLICATION LEVEL VALIDATION
    def clean(self):
        """
        Ensure:
        - user1 is always the user with the lower ID.
        - No self-chat is allowed (user1 != user2).
        - No duplicate chat exists.
        """
        # 1. Ensure user1 is always the smaller ID
        if self.user1_id > self.user2_id:
            self.user1, self.user2 = self.user2, self.user1

        # 2. Prevent self-chat
        if self.user1 == self.user2:
            raise ValidationError("A user cannot start a chat with themselves.")

        # 3. Prevent bidirectional duplicates
        if Chat.objects.filter(user1=self.user1, user2=self.user2).exists():
            raise ValidationError("A chat between these users already exists.")

    def save(self, *args, **kwargs):
        """
        Call clean() before saving to enforce validation.
        """
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        #DATABASE LEVEL VALIDATION
        constraints = [
            models.UniqueConstraint(
                fields=['user1', 'user2'],
                name='unique_chat_between_users'
            )
        ]


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)