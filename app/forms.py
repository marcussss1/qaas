from django import forms
from django.forms import CharField
from django.core.exceptions import ValidationError
from django.core import validators

# class UsernameField(CharField):
    # def validate(self, value):
#         super().validate(value)
#         if value == '123':
#             raise ValidationError("...")



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    login = forms.CharField()
    email = forms.EmailField()
    nickname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField()

    def clean_repeat_password(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['repeat_password']:
            raise ValidationError('Password do not match!')
        return cleaned_data
