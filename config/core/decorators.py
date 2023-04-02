from django.http import JsonResponse
from .models import Message,Thread
from functools import wraps
from django.shortcuts import get_object_or_404

def beMessageOwner(func):
    @wraps(func)
    def inner(request,threadId,messageId,*args,**kwargs):

        message=Message.objects.get(id=messageId)
        thread=get_object_or_404(Thread,id=threadId)
        
        if request.user.is_authenticated:
            if request.user == message.sender_user:
                return func(request,messageId,threadId,*args,**kwargs)
            else:
                return JsonResponse({"error":"not allowed"})
        else:
            return JsonResponse({"error":"login first"})
    return inner


