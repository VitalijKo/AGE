from django import forms
from django.contrib.auth.models import User
from .models import unitInfo


class unitForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'id': 'passwordfield', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'id': 'emailfield', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'id': 'usernamefield', 'class': 'form-control'})
        }


class unitInfoForm(forms.ModelForm):
    class Meta:
        model = unitInfo
        fields = ['address', 'subject', 'image']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'})
        }
