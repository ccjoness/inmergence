from .models import InmergenceUser
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    pass
    # class Meta:
    #     model = User


class UserProfileForm(forms.ModelForm):
    pass
    # class Meta:
    #     model = InmergenceUser
    #     exclude = ['user']