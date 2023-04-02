from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync
from .models import Message,Thread
import json
from channels.exceptions import StopConsumer
from accounts.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from channels.db import database_sync_to_async


class SingleChat(AsyncConsumer):

    async def websocket_connect(self,event):

        self.thread_id=self.scope["url_route"]["kwargs"]["id"]
        self.user=self.scope["user"]
        self.group_id=f"chat_{self.thread_id}"


        if self.user.is_authenticated:

            await self.channel_layer.group_add(
                self.group_id,
                self.channel_name
            )
            await self.send({
                "type":"websocket.accept"
            })
        else:
            await self.send({
                "type":"websocket.close"
            })

    async def websocket_disconnect(self,event):

        await self.channel_layer.group_discard(
            self.group_id,
            self.channel_name
        )        
        raise StopConsumer()
    
    async def websocket_receive(self,event):
        text_data=event.get("text",None)
        if text_data:
            text_data_json=json.loads(text_data)


            print(text_data_json)

            thread=await self.get_thread(threadId=text_data_json["thread_id"])
            S_u=await self.get_user(phone=text_data_json["sender"])
            R_u=await self.get_user(phone=text_data_json["receiver"])
            new_message=await self.create_message(
                text=text_data_json["text"],
                sender=S_u,
                receiver=R_u,
                thread=thread
            )




            await self.channel_layer.group_send(
                self.group_id,
                {
                    "type":"chat_message",
                    "message":json.dumps({

                        "text":text_data_json["text"],
                        "sender":text_data_json["sender"],
                        "receiver":text_data_json["receiver"],
                        "time":str(new_message.iranTimeCreated),
                        "id":new_message.id,
                        # "sender_user_phone_number":new_message.sender_user.phone_number
                        # "image":str(new_message.thread.commerical.commericalimage_set.first.image.url)
                    })
                }
            )


    async def chat_message(self,event):
        message=event["message"]
        await self.send({
            "type":"websocket.send",
            "text":message
        })
    


    @database_sync_to_async
    def get_thread(self,threadId):
        return get_object_or_404(Thread,id=threadId)


    @database_sync_to_async
    def get_user(self,phone):
        return get_object_or_404(User,phone_number=phone)


    @database_sync_to_async
    def create_message(self,text,sender,receiver,thread):
        new_message=Message(
            text=text,
            sender_user=sender,
            receiver_user=receiver,
            thread=thread
        )
        new_message.save()
        return new_message
    