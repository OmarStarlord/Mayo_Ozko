import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from .models import Message, Room

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handles WebSocket connection."""
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data["message"]
        sender_username = data["sender"]

        sender = await self.get_user(sender_username)
        room = await self.get_room(self.room_id)

        if sender and room:
            profile_picture = sender.profile_pic.url if sender.profile_pic else "/static/images/default.png"

            message = await self.create_message(room, sender, message_content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message_content,
                    "sender": sender.username,
                    "profile_picture": profile_picture
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "profile_picture": event["profile_picture"]
        }))

    @staticmethod
    async def get_user(username):
        """Fetches a user asynchronously."""
        close_old_connections()
        try:
            return await User.objects.aget(username=username)
        except User.DoesNotExist:
            return None

    @staticmethod
    async def get_room(room_id):
        """Fetches a chat room asynchronously."""
        close_old_connections()
        try:
            return await Room.objects.aget(id=room_id)
        except Room.DoesNotExist:
            return None

    @staticmethod
    async def create_message(room, sender, content):
        """Creates and saves a new chat message."""
        close_old_connections()
        return await Message.objects.acreate(room=room, sender=sender, content=content)
