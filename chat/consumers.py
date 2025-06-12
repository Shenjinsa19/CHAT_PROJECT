import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.other_username = self.scope["url_route"]["kwargs"]["username"]
        self.room_name = self.get_room_name(self.user.username, self.other_username)
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # async def receive(self, text_data):
    #     data = json.loads(text_data)
    #     message = data["message"]

    #     await self.save_message(self.user.username, self.other_username, message)

    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             "type": "chat_message",
    #             "message": message,
    #             "sender": self.user.username
    #         }
    #     )
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        try:
            await self.save_message(self.user.username, self.other_username, message)
        except Exception as e:
            print(f"[ERROR] Failed to save message: {e}")
            return

        await self.channel_layer.group_send(
           self.room_group_name,
           {
            "type": "chat_message",
            "message": message,
            "sender": self.user.username
            }
        )


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))

    def get_room_name(self, user1, user2):
        return "_".join(sorted([user1, user2]))

    @database_sync_to_async
    
    def save_message(self, sender, receiver, message):
        from django.contrib.auth.models import User
        from .models import Message
        print(f"[SAVE MESSAGE] From: {sender}, To: {receiver}, Message: {message}")
        from django.contrib.auth.models import User  # Import inside method to avoid app registry issues
        # sender_user = User.objects.get(username=sender)
        # receiver_user = User.objects.get(username=receiver)
        sender_user = User.objects.get(username__iexact=sender)
        receiver_user = User.objects.get(username__iexact=receiver)
        return Message.objects.create(sender=sender_user, receiver=receiver_user, text=message)
