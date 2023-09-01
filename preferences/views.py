from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ParticipantPreference


@login_required
def home(request):
    exists = ParticipantPreference.objects.filter(user=request.user).exists()

    participant_preferences = None

    if request.method == 'GET':
        mode = 'on'

        if exists:
            mode = 'off'

            participant_preferences = ParticipantPreference.objects.get(user=request.user)

            if participant_preferences.send_email:
                mode = 'on'

        context = {
            'participant_preferences': participant_preferences,
            'email_pref_value': mode
        }

        return render(request, 'preferences/home.html', context)

    if request.method == 'POST':
        if exists:
            mode = 'off'

            participant_preferences = ParticipantPreference.objects.get(user=request.user)

        preference = request.POST['email_pref'] == '1'

        if exists:
            participant_preferences.send_email = preference
            participant_preferences.save()

        else:
            mode = 'on'

            ParticipantPreference.objects.create(user=request.user, send_email=preference)

        participant_preferences = ParticipantPreference.objects.filter(user=request.user)

        if preference == 'True':
            mode = 'on'

        messages.success(request, f'Email Notifications are turned {mode}')

        context = {
            'participant_preferences': participant_preferences,
            'email_pref_value': mode
        }

        return render(request, 'preferences/home.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(request, 'Your password was successfully updated!')

            return redirect('participants:login')

        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form
    }

    return render(request, 'preferences/change-password.html', context)
