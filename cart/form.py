from django import forms
class profile_change_pass(forms.Form):
    last_password=forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password_con = forms.CharField(widget=forms.PasswordInput)
