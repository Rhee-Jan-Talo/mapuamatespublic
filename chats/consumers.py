import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from accounts.models import User as UserModel
from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from .models import ChatMessage, Thread


User = UserModel

class ChatConsumer(AsyncConsumer):

        

    async def websocket_connect(self, event):
        print("Connected: ", event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send(
            {
                'type':'websocket.accept'
            }
        )

    async def websocket_receive(self, event):
        print("Received: ", event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        thread_id = received_data.get('thread_id')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        sender_img = received_data.get('sender_img')
        print("**************")
        
        print(f"Thread ID: {thread_id}")
        print(f"Sent by: {sent_by_id}")
        print(f"message: {msg}")

        if not msg:
            print('Error: empty message')
            return False
        
        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)

        if not send_to_user:
            print('Error: send to user is incorrect')
        
        if not sent_by_user:
            print('Error: sent by user is incorrect')

        if not thread_obj:
            print('Error: thread id is incorrect')

        await self.save_to_db(thread_id, sent_by_id, msg)

        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']
        response = {
            'message':msg,
            'sent_by' : self_user.id,
            'thread_id': thread_id,
            'sender_img' :sender_img,
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type':'chat_message',
                'text': json.dumps(response)
            }
        )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type':'chat_message',
                'text': json.dumps(response)
            }
        )

        

    async def websocket_disconnect(self, event):
        print("Disconnected: ", event)
        raise StopConsumer()
    

    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type':'websocket.send',
            'text':event['text'],
        })

    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        print(f'user: {obj}')
        return obj
    
    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        print(f'thread: {obj}')
        return obj
    

    @database_sync_to_async
    def save_to_db(self, thread_id, sent_by_id, msg):
        ChatMessage.objects.create(
            thread = Thread.objects.get(id=thread_id),
            user = User.objects.get(id=sent_by_id),
            message = msg,
        )

            
        

        