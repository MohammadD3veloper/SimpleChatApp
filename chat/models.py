from django.db import models
from django.conf import settings
import uuid
from django.shortcuts import reverse, redirect


user = settings.AUTH_USER_MODEL


# Create your models here.
class Message(models.Model):
    text = models.TextField(max_length=500)
    sender = models.ForeignKey(user, on_delete=models.CASCADE, related_name="messages")
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name="messages")
    date = models.DateTimeField(auto_now=True)



class Members(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat_members', unique=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="member_on", unique=True)
    date_joined = models.DateTimeField(auto_now=True)


class Chat(models.Model):
    title = models.CharField(max_length=50)
    address = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    description = models.CharField(max_length=200, null=True, blank=True)
    admin = models.ForeignKey(user, on_delete=models.CASCADE, related_name="admin_on")
    private = models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse('chat:chat', kwargs={'uuid': self.address})

    def get_absolute_url_edit(self):
        return reverse('chat:update', kwargs={'uuid': self.address})
