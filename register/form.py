from django import forms
from django.core import validators
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class regisform(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_con = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
class loginform(forms.Form):
    email = forms.EmailField()

    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)