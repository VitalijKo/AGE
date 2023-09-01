import json
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from validate_email import validate_email
from .views import EmailThread


class UsernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)

        username = data['username']

        if not username.isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username Exists'}, status=409)

        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)

        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email exists'}, status=409)

        return JsonResponse({'email_valid': True})


class Cheating(View):
    def get(self, request, creatorname):
        participant = request.user.username

        email = User.objects.get(username=creatorname).email
        email_subject = 'Participant Cheating'
        email_body = 'Participant caught changing window for 5 times. Participant username is :' + participant
        email_from = 'noreply@game.com'
        email_obj = EmailMessage(
            email_subject,
            email_body,
            email_from,
            [email]
        )

        EmailThread(email_obj).start()

        return JsonResponse({'sent': True})
