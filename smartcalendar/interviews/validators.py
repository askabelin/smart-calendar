from datetime import datetime

from django.core.exceptions import ValidationError


def sharp_time(value):
    if not value.minute == 0:
        raise ValidationError('Minutes should be equal to zero')


def in_future(value):
    if value < datetime.now():
        raise ValidationError(f'{value}: should be in future')
