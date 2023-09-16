from django.contrib import admin
from .question_models import Question
from .question_paper_models import QuestionPaper
from .models import Game

admin.site.signup(Question)
admin.site.signup(QuestionPaper)
admin.site.signup(Game)
