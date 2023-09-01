import threading
from django.core.mail import EmailMessage
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.views import View
from django.shortcuts import render, redirect
from participants.views import EmailThread
from questions.views import has_group
from .forms import unitForm, unitInfoForm
from .models import unitInfo


class SignUpView(View):
    def get(self, request):
        unit_form = unitForm()
        unit_info_form = unitInfoForm()

        context = {
            'unit_form': unit_form,
            'unit_info_form': unit_info_form
        }

        return render(request, 'units/signup.html', context)

    def post(self, request):
        unit_form = unitForm(data=request.POST)
        unit_info_form = unitInfoForm(data=request.POST)
        
        email_to = request.POST['email']

        if unit_form.is_valid() and unit_info_form.is_valid():
            unit = unit_form.save()
            unit.set_password(unit.password)
            unit.is_active = True
            unit.is_staff = True
            unit.save()

            domain = get_current_site(request).domain
            
            email_subject = 'Activate your AGE unit account'
            email_body = f'Hello. Please contact the admin team of {domain} to sign up yourself as a creator.\n\nYou are receiving this message because you signed up on {domain}. If you didn\'t sign up please contact support team on {domain}'
            email_from = 'vitmihkov@ya.ru'
            
            email = EmailMessage(
                email_subject,
                email_body,
                email_from,
                [email_to]
            )
            
            participant_info = unit_info_form.save(commit=False)
            participant_info.user = unit
            
            if 'image' in request.FILES:
                participant_info.image = request.FILES['image']
                
            participant_info.save()
            
            messages.success(request, 'Successfull sign up. Check your email for confirmation')
            
            EmailThread(email).start()
            
            return redirect('units:login')
        
        else:
            context = {
                'unit_form': unit_form,
                'unit_info_form': unit_info_form
            }
            
            return render(request, 'units/signup.html', context)


class LoginView(View):
    def get(self, request):
        return render(request, 'units/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        group_member = False
        
        if username and password:
            user = auth.authenticate(username=username, password=password)

            exist = User.objects.filter(username=username).exists()
            
            if exist:
                user_ch = User.objects.get(username=username)

                group_member = has_group(user_ch, 'Creator')

            if user and user.is_active and exist and group_member:
                auth.login(request, user)

                messages.success(request, f'Welcome, {user.username}')

                return redirect('units:home')

            elif not group_member and exist:
                messages.error(request, 'You dont have permssions to login as units.')

                return render(request, 'units/login.html')

            messages.error(request, 'Invalid credentials')

            return render(request, 'units/login.html')

        messages.error(request, 'Please fill all fields')

        return render(request, 'units/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)

        messages.success(request, 'Logged out')

        return redirect('units:login')


@login_required(login_url='units:login')
def home(request):
    return render(request, 'units/home.html')
