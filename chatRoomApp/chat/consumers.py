from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('Hay conexion')
        await self.accept()
        await self.channel_layer.group_add(
            "chat",  # The name of the group
            self.channel_name
        )

    async def disconnect(self, close_code):
        print(f'Se cerro la conexion:{close_code}')

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # sender = text_data_json['sender']

        # print(message, sender)

        await self.send(text_data=json.dumps({
            'message':message,
            #'sender':sender
        }))
    
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'consumerMessage': message
        }))
