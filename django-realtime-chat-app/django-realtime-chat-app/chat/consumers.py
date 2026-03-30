import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone
from .models import Message, Notification, UserPresence


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user or isinstance(self.user, AnonymousUser):
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        event_type = data.get('type', 'message')

        if event_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_event',
                    'user': self.user.username,
                    'is_typing': data.get('is_typing', False),
                }
            )
            return

        receiver_username = data.get('receiver')
        content = data.get('message', '').strip()
        if not receiver_username or not content:
            return

        message = await self.save_message(self.user.username, receiver_username, content)
        unread_count = await self.get_unread_count(receiver_username, self.user.username)

        payload = {
            'type': 'chat_message',
            'message': message.content,
            'sender': self.user.username,
            'receiver': receiver_username,
            'timestamp': message.created_at.strftime('%d %b %Y, %I:%M %p'),
            'message_id': message.id,
            'unread_count': unread_count,
        }

        await self.channel_layer.group_send(self.room_group_name, payload)
        await self.channel_layer.group_send(
            f'notifications_{receiver_username}',
            {
                'type': 'notify_user',
                'sender': self.user.username,
                'message': message.content,
                'timestamp': payload['timestamp'],
                'unread_count': unread_count,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender': event['sender'],
            'receiver': event['receiver'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id'],
            'unread_count': event['unread_count'],
        }))

    async def typing_event(self, event):
        if event['user'] != self.user.username:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'user': event['user'],
                'is_typing': event['is_typing'],
            }))

    @database_sync_to_async
    def save_message(self, sender_username, receiver_username, content):
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        message = Message.objects.create(sender=sender, receiver=receiver, content=content)
        Notification.objects.create(user=receiver, message=message)
        return message

    @database_sync_to_async
    def get_unread_count(self, username, sender_username):
        receiver = User.objects.get(username=username)
        sender = User.objects.get(username=sender_username)
        return Message.objects.filter(sender=sender, receiver=receiver, is_read=False).count()


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user or isinstance(self.user, AnonymousUser):
            await self.close()
            return

        self.group_name = 'presence_global'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.set_presence(True)
        await self.channel_layer.group_send(
            self.group_name,
            {'type': 'presence_event', 'username': self.user.username, 'is_online': True}
        )

    async def disconnect(self, close_code):
        if getattr(self, 'user', None) and not isinstance(self.user, AnonymousUser):
            await self.set_presence(False)
            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'presence_event', 'username': self.user.username, 'is_online': False}
            )
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def presence_event(self, event):
        await self.send(text_data=json.dumps({
            'type': 'presence',
            'username': event['username'],
            'is_online': event['is_online'],
        }))

    @database_sync_to_async
    def set_presence(self, is_online):
        presence, _ = UserPresence.objects.get_or_create(user=self.user)
        presence.is_online = is_online
        presence.last_seen = timezone.now()
        presence.save(update_fields=['is_online', 'last_seen', 'updated_at'])


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if not self.user or isinstance(self.user, AnonymousUser):
            await self.close()
            return
        self.group_name = f'notifications_{self.user.username}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify_user(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'sender': event['sender'],
            'message': event['message'],
            'timestamp': event['timestamp'],
            'unread_count': event['unread_count'],
        }))
