from django.contrib.auth.models import User
from django.db import models


class ParticipantPreference(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    send_email = models.BooleanField('Email', default=True)

    def __str__(self):
        return f'{self.user}s preferences'

    class Meta:
        verbose_name = 'Предпочтение'
        verbose_name_plural = 'Предпочтения'
