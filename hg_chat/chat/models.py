from django.db import models
from django.contrib.auth.models import User
import uuid
import random

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    hg_id = models.CharField(max_length=10, unique=True, blank=True)

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    bio = models.TextField(blank=True)
    status = models.CharField(max_length=150, blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')

    is_online = models.BooleanField(default=False)   # ✅ ADD THIS

    def save(self, *args, **kwargs):
        if not self.hg_id:
            self.hg_id = "HG" + str(random.randint(10000, 99999))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')

    message = models.TextField()

    file = models.FileField(upload_to='chat_files/', blank=True, null=True)  # 📎 FILE

    is_read = models.BooleanField(default=False)  # ✔✔ READ RECEIPT

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"

# models.py
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    contact_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_by')

    saved_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user} saved {self.contact_user}"

from django.db import models
from django.contrib.auth.models import User


from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=100)

    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='group_admin',
        null=True,
        blank=True
    )

    members = models.ManyToManyField(
        User,
        related_name='chat_groups'   # 🔥 VERY IMPORTANT (fix clash error)
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    file = models.FileField(upload_to='group_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)  # ✅ ADD THIS


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='status/')
    text = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(hours=24))

    viewers = models.ManyToManyField(User, related_name='viewed_status', blank=True)

    def is_expired(self):
        return timezone.now() > self.expires_at

class Report(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    reason = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reported_by} reported {self.message.id}"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

class OnlineUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)