from django.contrib.auth.models import User
from django.db import models
from questions.question_models import Question
from questions.question_paper_models import QuestionPaper


class ParticipantInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    address = models.CharField('Адрес', max_length=256, blank=True)
    stream = models.CharField('Поток', max_length=64, blank=True)
    image = models.ImageField('Фото', upload_to='participants', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class ParticipantQuestion(Question):
    creator = None
    participant = models.ForeignKey(User, limit_choices_to={'groups__name': 'Participant'}, on_delete=models.CASCADE, null=True, verbose_name='Участник')
    choice = models.CharField('Выбор', max_length=4, default='E')

    def __str__(self):
        return str(self.participants.username) + ' ' + str(self.qno) + '-ParticipantQuestion'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class ParticipantGame(models.Model):
    participant = models.ForeignKey(User, limit_choices_to={'groups__name': 'Participant'}, on_delete=models.CASCADE, null=True, verbose_name='Участник')
    qpaper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, null=True, verbose_name='Билет')
    questions = models.ManyToManyField(ParticipantQuestion, verbose_name='Вопросы')
    game_name = models.CharField('Название', max_length=100)
    score = models.IntegerField('Счет', default=0)
    completed = models.IntegerField('Выполнено', default=0)

    def __str__(self):
        return str(self.participants.username) + ' ' + str(self.game_name) + ' ' + str(self.qpaper.title) + '-ParticipantGame'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class ParticipantResults(models.Model):
    participant = models.ForeignKey(User, limit_choices_to={'groups__name': 'Participant'}, on_delete=models.CASCADE, null=True, verbose_name='Участник')
    games = models.ManyToManyField(ParticipantGame, 'Игры')

    def __str__(self):
        return str(self.participants.username) + ' -ParticipantResults'

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
