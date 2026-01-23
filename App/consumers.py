import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated and self.user.is_staff:
            await self.channel_layer.group_add("notifications_staff",self.channel_name)
        else:
            await self.channel_layer.group_add("notifications_all",self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        if self.user.is_authenticated and self.user.is_staff:
            await self.channel_layer.group_discard("notifications_staff",self.channel_name)
        else:
            await self.channel_layer.group_discard("notifications_all",self.channel_name)

    async def receive(self, text_data):
        pass

    async def notify(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
