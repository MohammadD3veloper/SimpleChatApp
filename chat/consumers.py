import json
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from .models import Message, Chat
from django.contrib.auth import get_user_model



class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.user = self.scope['user']
        self.chat_id = self.scope["url_route"]["kwargs"]["uuid"]
        self.chat = await self.get_chat_by_uuid(self.chat_id)
        self.chat_room_uuid = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(
            self.chat_room_uuid,
            self.channel_name
        )


        await self.send({
            "type": "websocket.accept"
        })

        await self.channel_layer.group_send(
            self.chat_room_uuid,
            {
                "type": "chat_activity",
                "message": self.user.username,
            }
        )

    
    async def websocket_disconnect(self, code):
        await self.channel_layer.group_send(
            self.chat_room_uuid,
            {
                "type": "chat_activity",
                "message": self.user.username,
            }
        )

        await self.channel_layer.group_discard(
            self.chat_room_uuid,
            self.channel_name
        )

        raise StopConsumer()


    async def websocket_receive(self, event):
        text_data = event.get('text', None)
        bytes_data = event.get('bytes', None)
        if text_data:
            text_data_json = json.loads(text_data)
            text = text_data_json['text']
            msg = await self.write_data_on_db(text)
            data = {
                "sender": self.user.username,
                "text": msg.text,
                "date": str(msg.date)
            }
            await self.channel_layer.group_send(
                self.chat_room_uuid,
                {
                    "type": "chat_message",
                    "message": json.dumps(data),
                    "sender_channel_name": self.channel_name
                }
            )

    async def chat_message(self, event):
        message = event["message"]

        await self.send({
            "type": "websocket.send",
            "text": message
        })

    async def chat_activity(self, event):
        message = event.get('leave')
        await self.send({
            "type": "websocket.send",
            "leave": message
        })
        if not message:
            message = event.get('join')
            await self.send({
                "type": "websocket.send",
                "join": message
            })
        


    @database_sync_to_async
    def write_data_on_db(self, text: str):
        msg = Message.objects.create(
            text=text,
            sender=self.user,
            chat=self.chat,
        )
        return msg


    @database_sync_to_async
    def get_chat_by_uuid(self, uuid):
        chat = Chat.objects.get(address=uuid)
        return chat
