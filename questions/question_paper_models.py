from django.db import models
from django import forms
from django.contrib.auth.models import User
from .question_models import Question


class QuestionPaper(models.Model):
    creator = models.ForeignKey(User, limit_choices_to={'groups__name': 'Creator'}, on_delete=models.CASCADE, verbose_name='Создатель')
    title = models.CharField('Название', max_length=128)
    questions = models.ManyToManyField(Question, verbose_name='Вопросы')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'


class QPForm(forms.ModelForm):
    def __init__(self, creator, *args, **kwargs):
        super(QPForm, self).__init__(*args, **kwargs)

        self.fields['questions'].queryset = Question.objects.filter(creator=creator)

    class Meta:
        model = QuestionPaper
        fields = '__all__'
        exclude = ['creator']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
