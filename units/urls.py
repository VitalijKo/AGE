from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'units'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='units/reset-password.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='units/reset-password-sent.html'), name='reset_password_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='units/set-new-password.html'), name='reset_password_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='units/reset-password-done.html'), name='reset_password_confirm')
]
