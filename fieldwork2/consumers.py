from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
from django.core.mail import send_mail
from Saudit.settings import EMAIL_HOST_USER
from .models import ChatMessage,ConnectedUser
from audit_plan_setup.models import Auditor, Auditee


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def fetch_old_messages(self, room_name):
        # Fetch older messages from the database for the given room
        older_messages = ChatMessage.objects.filter(room_name=room_name)
        messages = [{'message': message.content, 'username': message.sender.username} for message in
                    older_messages]
        return messages

    @database_sync_to_async
    def record_connected_user(self, username):
        print("calling")
        # Retrieve the list of connected users for the specific room
        connected_user, created = ConnectedUser.objects.get_or_create(user=self.scope['user'], room_name=self.room_name)
        print(connected_user)
        connected_users = ConnectedUser.objects.filter(room_name=self.room_name).exclude(user=self.scope['user'])
        return [user.user.username for user in connected_users]

    async def connect(self):
        # Get the room_name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # Proceed with the connection
        self.room_group_name = 'chat_%s' % self.room_name
        print(f"User connected to {self.room_group_name}")

        # Store the username of the connected user
        connected_users = await self.record_connected_user(self.scope["user"].username)

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send the list of connected users to the connected client
        await self.send(text_data=json.dumps({'connected_users': connected_users}))

        older_messages = await self.fetch_old_messages(self.room_name)
        for message in older_messages:
            await self.send(text_data=json.dumps(message))


    async def disconnect(self, close_code):
        # Leave the room group
        print(f"User disconnected from {self.room_group_name}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if 'type' in text_data_json:
            message_type = text_data_json['type']

            if message_type == 'mention.suggestions':
                # Handle mention suggestions
                query = text_data_json.get('query', '')
                await self.send_mention_suggestions(self.room_name, query)
                return
        message = text_data_json['message']
        username = text_data_json['username']

        print(f"Received message: {message}")

        if '@' in message:
            # Extract the query after '@'
            query = message.split('@')[-1].strip()
            print(query)

            # Send mention suggestions to the user
            await self.send_mention_suggestions(self.room_name, query)

        # Send the received message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'username': username,
            }
        )

    async def send_email_notification(self, recipient_email, sender_username, room_name):
        subject = f'You were mentioned in the chat room {room_name}'
        message = f'Hello,\n\n{sender_username} mentioned you in the chat room {room_name}.\n\nVisit the chat room to view the message.'
        from_email = EMAIL_HOST_USER
        recipient_list = [recipient_email]
        send_mail(subject, message, from_email, recipient_list)

    async def notify_user_email(self, mentioned_username, room_name, sender_name):
        user = await database_sync_to_async(User.objects.select_related('auditor', 'auditee').get)(
            username=mentioned_username)
        print(user)
        recipient_email = user.email
        print(recipient_email)
        await self.send_email_notification(recipient_email=recipient_email,sender_username=sender_name,room_name=room_name)

    @database_sync_to_async
    def save_chat_message(self, sender, room_name, message):
        chat_message = ChatMessage(sender=sender, room_name=room_name, content=message)
        chat_message.save()

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        user = await database_sync_to_async(User.objects.select_related('auditor', 'auditee').get)(username=username)
        sender = user

        room_name = self.room_name
        await self.save_chat_message(sender, room_name, message)
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({'message': message, 'username': username}))

        mentioned_usernames = [word[1:] for word in message.split() if word.startswith('@')]
        for mentioned_username in mentioned_usernames:
            sender_username = sender.username
            print(sender_username)
            print("sending")
            await self.notify_user_email(mentioned_username, room_name, sender_name=sender_username)

    async def send_mention_suggestions(self, room_name, query):
        # Get the list of connected users for the specific room
        connected_users = await self.fetch_connected_users(room_name)

        # Filter the connected users based on the query
        suggestions = [user for user in connected_users if query.lower() in user.lower()]

        # Send the suggestions to the user
        await self.send(text_data=json.dumps({'type': 'mention.suggestions', 'suggestions': suggestions}))

    @database_sync_to_async
    def fetch_connected_users(self, room_name):
        # Fetch connected users for the specific room
        connected_users = ConnectedUser.objects.filter(room_name=room_name).exclude(user=self.scope['user'])
        return [user.user.username for user in connected_users]
