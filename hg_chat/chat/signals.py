from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(user_logged_in)
def user_online(sender, request, user, **kwargs):
    Profile.objects.filter(user=user).update(is_online=True)

@receiver(user_logged_out)
def user_offline(sender, request, user, **kwargs):
    Profile.objects.filter(user=user).update(is_online=False)