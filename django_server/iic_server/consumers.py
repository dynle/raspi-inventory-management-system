import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("info_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("info_group", self.channel_name)

    def receive(self, message, product):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message, "product": product}
        )

    async def send_message(self, event):
        message = event['message']
        product = event['product']
        await self.send(text_data=json.dumps({
            'message': message,
            'product': product
        }))