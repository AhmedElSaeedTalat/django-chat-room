from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
""" creation of forms needed for the application """


class CustomUserCreationForm(UserCreationForm):
    """ custom for for registration """
    class Meta(UserCreationForm.Meta):
        """ exclude username field """
        fields = ('email', 'password1', 'password2')

    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        """ validate email """
        email = self.cleaned_data['email'].lower()
        user = User.objects.filter(email=email).first()
        if user:
            raise ValidationError('Email exists')
        return email

    def clean_password2(self):
        """ validate password """
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('password dont match')
        return password1

    def save(self, commit=True):
        """ save user """
        username = self.cleaned_data['email'].split('@')[0]
        user = User.objects.create(
            username=username,
            email=self.cleaned_data['email'],
            password=make_password(self.cleaned_data['password1'])
        )
        return user