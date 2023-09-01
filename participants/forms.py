from django import forms
from django.contrib.auth.models import User
from .models import ParticipantInfo


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'id': 'passwordfield', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'id': 'emailfield', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'id': 'usernamefield', 'class': 'form-control'})
        }


class ParticipantInfoForm(forms.ModelForm):
    class Meta:
        model = ParticipantInfo
        fields = ['address', 'stream', 'image']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'stream': forms.TextInput(attrs={'class': 'form-control'})
        }
