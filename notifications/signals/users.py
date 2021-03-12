from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models.user import User
from users.models.invites import Invite

@receiver(post_save, sender=User)
def create_or_update_user(sender, instance, created, **kwargs):
    if created:
        Invite.objects.bulk_create([
            Invite(owner=instance) for i in range(settings.NEW_USER_INVITES)
        ])
