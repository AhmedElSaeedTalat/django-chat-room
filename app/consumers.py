from channels.generic.websocket import AsyncWebsocketConsumer
import json
import redis
class ChatRoomConsumer(AsyncWebsocketConsumer):
    """ class for web socket connection and sending and receiveing """
    async def connect(self):
        """
        connect to web socket, get chat room name from url, create group, add group name
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        """ this one to accept connection """
        await self.accept()

        """ send message to all group members """
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tester_message',
                'tester': 'hello world'
            }
        )
    
    async def tester_message(self, event):
        """ send message to all as for testing """
        tester = event['tester']
        await self.send(text_data=json.dumps({
            'tester': tester
        }))

    async def disconnect(self, close_code):
        """ desconnect websocket """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """ receive sent message """
        info = json.loads(text_data)
        message = info['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
            )

    async def chat_message(self, event):
        """
            send message received back to chat room trough web socket so all can see it
        """
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))