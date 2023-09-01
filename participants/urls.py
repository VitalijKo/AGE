from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from . import api, views

app_name = 'participants'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('username-validate', api.UsernameValidation.as_view(), name='validate_username'),
    path('email-validate', api.EmailValidationView.as_view(), name='validate_email'),
    path('cheat/<str:creatorname>', api.Cheating.as_view(), name='cheat'),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='participants/reset-password.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='participants/reset-password-sent.html'), name='reset_password_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='participants/set-new-password.html'), name='reset_password_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='participants/reset-password-done.html'), name='reset_password_complete')
]
