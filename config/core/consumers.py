from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync
from .models import Message
import json
from channels.exceptions import StopConsumer
from accounts.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
