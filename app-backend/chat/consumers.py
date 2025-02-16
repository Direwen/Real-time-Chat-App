import json
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessage, Chat
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import ChatMessageSerializer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        print(self.user)
        if self.user.is_anonymous:
            self.close()
        else:
            self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
            self.chat_group_name = f"chat_{self.chat_id}"
            
            #add user to chat group
            async_to_sync(self.channel_layer.group_add)(
                self.chat_group_name,
                self.channel_name
            )
            
            self.accept()
            print(f"WebSocket connection established for {self.user.username}.")

    def disconnect(self, close_code):
        #Remove the user from the chat group
        async_to_sync(self.channel_layer.group_discard) (
            self.chat_group_name,
            self.channel_name
        )
        print(f"WebSocket connection closed with code: {close_code}")

    def receive(self, text_data=None, bytes_data=None):
        try:
            if text_data:
                text_data_json = json.loads(text_data)  # Use json.loads for strings
                message = text_data_json.get("message")
                chat_id = text_data_json.get("chat_id")
                
                #Save the message to the database
                chat_message = ChatMessage.objects.create(
                    chat=Chat.objects.get(pk=chat_id),
                    message=message,
                    sender=self.user
                )
                
                async_to_sync(self.channel_layer.group_send)(
                    self.chat_group_name,
                    {
                        "type": "chat_message",
                        "message": ChatMessageSerializer(chat_message).data,
                        "sender": self.user.username
                    }
                )
            else:
                print("No text data received.")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON data: {text_data}. Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    #Handler for sending messages to the group
    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        #Send the message to the websocket
        self.send(text_data=json.dumps({
            "message": message,
            "sender": sender
        }))