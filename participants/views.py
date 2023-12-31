import threading
from django.core.mail import EmailMessage
from django.contrib import auth, messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect
from preferences.models import ParticipantPreference
from .forms import ParticipantForm, ParticipantInfoForm
from .utils import account_activation_token


class SignUpView(View):
    def get(self, request):
        participant_form = ParticipantForm()
        participant_info_form = ParticipantInfoForm()

        context = {
            'participant_form': participant_form,
            'participant_info_form': participant_info_form
        }

        return render(request, 'participants/signup.html', context)

    def post(self, request):
        participant_form = ParticipantForm(data=request.POST)
        participant_info_form = ParticipantInfoForm(data=request.POST)

        email_to = request.POST['email']

        if participant_form.is_valid() and participant_info_form.is_valid():
            participant = participant_form.save()
            participant.set_password(participant.password)

            participant.is_active = False

            group = Group.objects.get_or_create(name='Participant')
            group[0].user_set.add(participant)

            participant.save()

            uidb64 = urlsafe_base64_encode(force_bytes(participant.pk))

            domain = get_current_site(request).domain

            reverse_kwargs = {
                'uidb64': uidb64,
                'token': account_activation_token.make_token(participant)
            }

            link = reverse('participants:activate', kwargs=reverse_kwargs)

            activate_url = f'http://{domain}{link}'
            email_subject = 'Activate your AGE account'
            email_body = f'Please use this link to confirm your account:\n{activate_url}\n\n\n\nYou are receiving this message because you signed up on {domain}. If this is not you, please contact support at {domain}.'
            email_from = 'vitmihkov@yandex.ru'
            email = EmailMessage(
                email_subject,
                email_body,
                email_from,
                [email_to]
            )

            participant_info = participant_info_form.save(commit=False)

            participant_info.user = participant

            if 'image' in request.FILES:
                participant_info.image = request.FILES['image']

            participant_info.save()

            messages.success(request, 'Signed up successfully. Check your email for confirmation')

            EmailThread(email).start()

            return redirect('participants:login')

        context = {
            'participant_form': participant_form,
            'participant_info_form': participant_info_form
        }

        return render(request, 'participants/signup.html', context)


class LoginView(View):
    def get(self, request):
        return render(request, 'participants/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            exist = User.objects.filter(username=username).exists()

            if exist:
                user_ch = User.objects.get(username=username)

                if user_ch.is_staff:
                    messages.error(
                        request,
                        'You are trying to log in as a participant, but you signed up as a creator. You will be redirected to the creator login. If you have trouble logging in, please reset your password or contact an administrator.',
                    )

                    return redirect('units:login')

            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                auth.login(request, user)

                messages.success(request, f'Welcome, {user.username}')

                return redirect('participants:home')

            else:
                user_n = User.objects.filter(username=username).exists()
                if user_n:
                    user_v = User.objects.get(username=username)

                    if user_v.is_active:
                        messages.error(request, 'Invalid credentials')

                        return render(request, 'participant/login.html')

                    messages.error(request, 'Account not activated')

                    return render(request, 'participant/login.html')

        messages.error(request, 'Please fill all fields')

        return render(request, 'participants/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)

        messages.success(request, 'Logged out')

        return redirect('participants:login')


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email

        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                messages.error(request, 'User already activated. Please proceed with login')

                return redirect('participants:login')

            if user.is_active:
                return redirect('participants:login')

            user.is_active = True

            user.save()

            messages.success(request, 'Account activated sucessfully')

            return redirect('participants:login')
        except Exception as e:
            raise e

        return redirect('participants:login')


@login_required
def home(request):
    return render(request, 'participants/home.html')
