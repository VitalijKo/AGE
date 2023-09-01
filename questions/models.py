from django import forms
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from .question_paper_models import QuestionPaper


class Game(models.Model):
    creator = models.ForeignKey(User, limit_choices_to={'groups__name': 'Creator'}, on_delete=models.CASCADE, verbose_name='Создатель')
    name = models.CharField('Название', max_length=64)
    total_marks = models.IntegerField('Оценки')
    QuestionPaper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, related_name='games', verbose_name='Билет')
    start_time = models.DateTimeField('Начало', default=datetime.now())
    end_time = models.DateTimeField('Конец', default=datetime.now())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class GameForm(forms.ModelForm):
    def __init__(self, creator, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)

        self.fields['QuestionPaper'].queryset = QuestionPaper.objects.filter(creator=creator)

    class Meta:
        model = Game
        fields = '__all__'
        exclude = ['creator']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control'})
        }
