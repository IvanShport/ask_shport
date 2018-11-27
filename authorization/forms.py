from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from authorization.models import Profile
from django.shortcuts import get_object_or_404

class LoginForm(forms.Form):
    login = forms.CharField(label='Логин', max_length=64,
                               widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Логин', 'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}))

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['login']
            password = self.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Неверный логин / пароль')

class RegForm(UserCreationForm):
    avatar = forms.ImageField(label='Аватар', required=False, widget=forms.FileInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")
        widgets = {'password'}

    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.__class__ == forms.widgets.FileInput:
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control-file'
                else:
                    field.widget.attrs.update({'class': 'form-control-file'})
            else:
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data['username']
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Данный логин уже занят")
        return username

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['password1']
        )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile = Profile()
        profile.user = user
        profile.avatar = self.cleaned_data['avatar']
        profile.save()

        return profile

class SettingsForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', min_length=4, max_length=150, required=False)
    avatar = forms.ImageField(label='Аватар', required=False, widget=forms.FileInput)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.__class__ == forms.widgets.FileInput:
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control-file'
                else:
                    field.widget.attrs.update({'class': 'form-control-file'})
            else:
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        try:
            username = self.cleaned_data['username']
        except KeyError:
            username = ''
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Данный логин уже занят")
        return username

    def clean_first_name(self):
        try:
            first_name = self.cleaned_data['first_name']
        except KeyError:
            first_name = ''
        return first_name

    def clean_last_name(self):
        try:
            last_name = self.cleaned_data['last_name']
        except KeyError:
            last_name = ''
        return last_name

    def clean_avatar(self):
        try:
            avatar = self.cleaned_data['avatar']
        except KeyError:
            avatar = ''
        return avatar

    def save(self, request):
        person = get_object_or_404(Profile, user=request.user)
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        avatar = self.cleaned_data['avatar']

        if username != '':
            person.user.username = username
        if first_name != '':
            person.user.first_name = first_name
        if last_name != '':
            person.user.last_name = last_name
        if avatar != '':
            person.avatar = avatar

        person.user.save()
        person.save()

        return person
