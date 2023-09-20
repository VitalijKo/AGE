from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('creator/games/', views.games_creator, name='games'),
    path('creator/previous-games/', views.previous_games_creator, name='previous_games'),
    path('creator/results/', views.display_results_creator, name='results'),
    path('creator/add-questions/', views.add_questions, name='add_questions'),
    path('creator/add-question-paper/', views.add_question_paper, name='add_question_paper'),
    path('creator/participants/', views.participants_creator, name='participants'),
    path('participant/games/', views.game_participant, name='game_participant'),
    path('participant/previous/', views.previous_participant, name='previous_participant'),
    path('participant/attendance/', views.participant_attendance, name='participant_attendance'),
    path('participant/display/<int:id>', views.get_game, name='game'),
    path('participant/result/<int:id>', views.get_result, name='result')
]
