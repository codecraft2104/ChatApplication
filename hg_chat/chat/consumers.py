import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.receiver_id = self.scope['url_route']['kwargs']['user_id']

        self.room_group_name = f"chat_{min(self.user.id, int(self.receiver_id))}_{max(self.user.id, int(self.receiver_id))}"

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

    async def receive(self, text_data):
        data = json.loads(text_data)

        # typing
        if 'typing' in data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing',
                    'user': self.user.username,
                    'typing': data['typing']
                }
            )
            return

        message = data.get('message', '')

        receiver = await sync_to_async(User.objects.get)(id=self.receiver_id)

        msg = await sync_to_async(Message.objects.create)(
            sender=self.user,
            receiver=receiver,
            message=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def typing(self, event):
        await self.send(text_data=json.dumps(event))