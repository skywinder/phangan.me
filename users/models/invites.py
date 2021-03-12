from uuid import uuid4

from django.db import models
from django.urls import reverse

from users.models.user import User


class Invite(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invites")
    membership_days = models.PositiveSmallIntegerField(default=30)
    used_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return f'{reverse("apply_invite")}?code={self.id}'
