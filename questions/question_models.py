from django.db import models
from django import forms
from django.contrib.auth.models import User


class Question(models.Model):
    creator = models.ForeignKey(User, limit_choices_to={'groups__name': 'Creator'}, on_delete=models.CASCADE, null=True, verbose_name='Создатель')
    qno = models.AutoField(primary_key=True, verbose_name='Номер')
    question = models.CharField('Вопрос', max_length=128)
    optionA = models.CharField('Вариант ответа 1', max_length=128)
    optionB = models.CharField('Вариант ответа 2', max_length=128)
    optionC = models.CharField('Вариант ответа 3', max_length=128)
    optionD = models.CharField('Вариант ответа 4', max_length=100)
    answer = models.CharField('Ответ', max_length=256)
    max_marks = models.IntegerField('Максимальные оценки', default=0)

    def __str__(self):
        return f'Вопрос №{self.qno}: {self.question} \t\t Варианты ответа: \nA. {self.optionA} \nB. {self.optionB} \nC. {self.optionC} \nD. {self.optionD} '

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class QForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ['qno', 'creator']
        widgets = {
            'question': forms.TextInput(attrs = {'class': 'form-control'}),
            'optionA': forms.TextInput(attrs = {'class': 'form-control'}),
            'optionB': forms.TextInput(attrs = {'class': 'form-control'}),
            'optionC': forms.TextInput(attrs = {'class': 'form-control'}),
            'optionD': forms.TextInput(attrs = {'class': 'form-control'}),
            'answer': forms.TextInput(attrs = {'class': 'form-control'}),
            'max_marks': forms.NumberInput(attrs = {'class': 'form-control'})
        }
