from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class regisform(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_con = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class loginform(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)

    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class forgetform(forms.Form):
    email = forms.EmailField()


class resetform(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_con = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        password_con = self.cleaned_data.get('confirm_password')

        if password == password_con:
            return password_con

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')
