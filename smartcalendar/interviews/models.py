from datetime import timedelta
from functools import lru_cache

from django.contrib.auth.models import Group
from django.db import models
from django.conf import settings

from .validators import sharp_time


@lru_cache()
def get_interviewers_group():
    return Group.objects.get(name='interviewers')


@lru_cache()
def get_candidates_group():
    return Group.objects.get(name='candidates')


class AvailableSlot(models.Model):
    """
    1-hour long interview slot that spreads from the beginning of any hour until the beginning of the next hour
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='slots')
    start = models.DateTimeField(validators=(sharp_time,))

    class Meta:
        unique_together = ('user', 'start')

    @property
    def end(self):
        return self.start + timedelta(hours=1)

    def __str__(self):
        return f'{self.user}: {self.start} - {self.end}'
