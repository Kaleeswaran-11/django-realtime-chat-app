from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserPresence


@receiver(post_save, sender=User)
def create_user_presence(sender, instance, created, **kwargs):
    if created:
        UserPresence.objects.create(user=instance)
