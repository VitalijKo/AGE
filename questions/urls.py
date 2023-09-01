from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('creator/view-games/', views.view_games_creator, name='view_games'),
    path('creator/view-previous-games/', views.view_previous_games_creator, name='previous_games'),
    path('creator/view-results/', views.view_results_creator, name='view_results'),
    path('creator/add-questions/', views.add_questions, name='add_questions'),
    path('creator/add-question-paper/', views.add_question_paper, name='add_question_paper'),
    path('creator/view-participants/', views.view_participants_creator, name='view_participants'),
    path('participant/view-games/', views.view_games_participant, name='view_games_participant'),
    path('participant/previous/', views.participant_view_previous, name='participant_view_previous'),
    path('participant/attendance/', views.view_participant_attendance, name='view_participant_attendance'),
    path('participant/appear/<int:id>', views.appear_game, name='appear_game'),
    path('participant/result/<int:id>', views.result, name='result')
]
