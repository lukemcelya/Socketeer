from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='rooms')

    def _str_(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user}: {self.text[:30]}"