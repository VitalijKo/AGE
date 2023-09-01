from django.contrib.auth.models import User
from django.db import models


class unitInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    address = models.CharField('Адрес', max_length=256, blank=True)
    subject = models.CharField('Предмет', max_length=64, blank=True)
    image = models.ImageField('Фото', upload_to='units', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'
