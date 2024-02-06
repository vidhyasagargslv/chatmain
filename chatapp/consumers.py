
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Room


class ChatConsumer(WebsocketConsumer): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}' 
        # self.room = Room.objects.get(name=self.room_name)


        
        #! connection has to be accepted
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        

    def disconnect(self, close_code):
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data_json,
            }
        )

    def chat_message(self, event):
    # Fetch the room when you actually need it
        self.room = Room.objects.get(name=self.room_name)

    # Get the message here
        message = event['message']

    # If the message is a dictionary, extract the actual message string
        if isinstance(message, dict) and 'message' in message:
            message = message['message']

        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
        }))