from django.contrib import admin
from .models import ParticipantInfo, ParticipantQuestion, ParticipantGame, ParticipantResults

admin.site.register(ParticipantInfo)
admin.site.register(ParticipantQuestion)
admin.site.register(ParticipantGame)
admin.site.register(ParticipantResults)
