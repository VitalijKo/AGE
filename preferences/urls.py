from django.urls import path
from . import views

app_name = 'preferences'

urlpatterns = [
    path('', views.home, name='home'),
    path('change-password/', views.change_password, name='change_password')
]
