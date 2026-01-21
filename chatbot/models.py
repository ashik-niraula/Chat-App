from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Chat(models.Model):
    id = models.UUIDField(unique=True,primary_key=True, editable=False,default=uuid.uuid4)
    text = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField( auto_now_add=True) 
    image = models.ImageField(blank=True,null=True,upload_to="chat_image/")
    

    def __str__(self):
        return self.text[:20]
    
    class Meta:
        ordering = ['created_at']

class Room(models.Model):
    id = models.UUIDField(unique=True,primary_key=True, editable=False,default=uuid.uuid4)
    chat = models.ManyToManyField(Chat,related_name='chat')
    user = models.ForeignKey(User, related_name="room_user", on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return f"{self.title if self.title else ''} -- {self.user.username}"
    
    class Meta:
        ordering = [f'{'-updated_at' if '-updated_at' else '-created_at' }']
    
    

