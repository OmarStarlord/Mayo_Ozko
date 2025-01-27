import json
import pusher
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from .models import Message, Room

# Pusher client setup
pusher_client = pusher.Pusher(
    app_id='1931997',
    key='b47d20482e4df2bf538c',
    secret='e280f4c8b43ecfff83b4',
    cluster='eu',
    ssl=True
)

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handles WebSocket connection."""
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        # Accept WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection."""
        pass  # No longer needed to handle group discard since Pusher is used

    async def receive(self, text_data):
        """Handles the received message from WebSocket and sends it to Pusher."""
        data = json.loads(text_data)
        message_content = data["message"]
        sender_username = data["sender"]

        sender = await self.get_user(sender_username)
        room = await self.get_room(self.room_id)

        if sender and room:
            profile_picture = sender.profile_pic.url if sender.profile_pic else "/static/images/default.png"

            # Create the message and save it to the database
            message = await self.create_message(room, sender, message_content)

            # Send the message to Pusher
            pusher_client.trigger(self.room_group_name, 'new_message', {
                'message': message_content,
                'sender': sender.username,
                'profile_picture': profile_picture
            })

    async def chat_message(self, event):
        """Handle incoming messages from Pusher and send them to the WebSocket."""
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
