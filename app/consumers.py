from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
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
        """ create session to save messages """
        self.session = self.scope['session']
        if 'messages' not in self.session:
            self.session['messages'] = []
        """ this one to accept connection """
        await self.accept()
        """ 
            check if there are saved messages
            if true: call send_msg to send saved
            msgs to newly connected user
        """
        if 'messages' in self.session:
            if len(self.session['messages']) > 0:
                await self.send_msg()

    async def send_msg(self):
        """ send message to newly connected users """
        await self.send(text_data=json.dumps({
            'type': 'saved_msg',
            'saved_msg': self.session['messages']
        }))

    async def disconnect(self, close_code):
        """ desconnect websocket """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """ 
            receive sent message
            publish received msgs
        """
        info = json.loads(text_data)
        message = info['message']
        username = info['username']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
            )

    async def chat_message(self, event):
        """
            send message received back to chat room trough web socket so all can see it
        """
        message = event['message']
        username = event['username']
        """ 
            save sent messages in session list
            clear session if messsages are more
            than 4 messages and start saving again
        """
        if len(self.session['messages']) <= 4:
            self.session['messages'].append({'message': message, 'user': username})
            await sync_to_async(self.session.save)()
        else:
            self.session['messages'].clear()
            await sync_to_async(self.session.save)()
            self.session['messages'].append({'message': message, 'user': username})
            await sync_to_async(self.session.save)()

        data = {
            'username': username,
            'msg': message
        }
        await self.send(text_data=json.dumps(data))