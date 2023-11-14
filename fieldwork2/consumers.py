from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from django.contrib.auth.models import User
from django.core.mail import send_mail

from Saudit.settings import EMAIL_HOST_USER
from .models import ChatMessage
from audit_plan_setup.models import Auditor, Auditee


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def fetch_old_messages(self, room_name):
        # Fetch older messages from the database for the given room
        older_messages = ChatMessage.objects.filter(room_name=room_name)
        messages = [{'message': message.content, 'username': message.sender.username} for message in
                    older_messages]
        return messages

    async def connect(self):
        # Get the room_name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(f"User connected to {self.room_group_name}")
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
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
        message = text_data_json['message']
        username = text_data_json['username']

        print(f"Received message: {message}")

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
