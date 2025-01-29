import json
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessage, Chat

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        print(self.user)
        if self.user.is_anonymous:
            self.close()
        else:
            self.accept()
            print(f"WebSocket connection established for {self.user.username}.")

    def disconnect(self, close_code):
        print(f"WebSocket connection closed with code: {close_code}")

    def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
                text_data_json = json.loads(text_data)  # Use json.loads for strings
                message = text_data_json.get("message")
                chat_id = text_data_json.get("chat_id")
                
                ChatMessage.objects.create(
                    chat=Chat.objects.get(pk=chat_id),
                    message=message,
                    sender=self.user
                )

                self.send(text_data=json.dumps({
                    "message": f"Stored a new message sent from {self.user.username}"
                }))
            else:
                print("No text data received.")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON data: {text_data}. Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")