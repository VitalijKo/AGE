from django.contrib import admin
from .models import ParticipantInfo, ParticipantQuestion, ParticipantGame, ParticipantResults

admin.site.signup(ParticipantInfo)
admin.site.signup(ParticipantQuestion)
admin.site.signup(ParticipantGame)
admin.site.signup(ParticipantResults)
