# Generated by Django 4.1.7 on 2023-08-20 11:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('qno', models.AutoField(primary_key=True, serialize=False, verbose_name='Номер')),
                ('question', models.CharField(max_length=128, verbose_name='Вопрос')),
                ('optionA', models.CharField(max_length=128, verbose_name='Вариант ответа 1')),
                ('optionB', models.CharField(max_length=128, verbose_name='Вариант ответа 2')),
                ('optionC', models.CharField(max_length=128, verbose_name='Вариант ответа 3')),
                ('optionD', models.CharField(max_length=100, verbose_name='Вариант ответа 4')),
                ('answer', models.CharField(max_length=256, verbose_name='Ответ')),
                ('max_marks', models.IntegerField(default=0, verbose_name='Максимальные оценки')),
                ('creator', models.ForeignKey(limit_choices_to={'groups__name': 'Creator'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='QuestionPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название')),
                ('creator', models.ForeignKey(limit_choices_to={'groups__name': 'Creator'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('questions', models.ManyToManyField(to='questions.question', verbose_name='Вопросы')),
            ],
            options={
                'verbose_name': 'Билет',
                'verbose_name_plural': 'Билеты',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('total_marks', models.IntegerField(verbose_name='Оценки')),
                ('start_time', models.DateTimeField(default=datetime.datetime(2023, 8, 20, 15, 0, 41, 842839), verbose_name='Начало')),
                ('end_time', models.DateTimeField(default=datetime.datetime(2023, 8, 20, 15, 0, 41, 842839), verbose_name='Конец')),
                ('QuestionPaper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='questions.questionpaper', verbose_name='Билет')),
                ('creator', models.ForeignKey(limit_choices_to={'groups__name': 'Creator'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
            ],
            options={
                'verbose_name': 'Игра',
                'verbose_name_plural': 'Игры',
            },
        ),
    ]
