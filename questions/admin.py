from django.contrib import admin
from .question_models import Question
from .question_paper_models import QuestionPaper
from .models import Game

admin.site.register(Question)
admin.site.register(QuestionPaper)
admin.site.register(Game)
