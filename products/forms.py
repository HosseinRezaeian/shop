from django import forms
from django.core.exceptions import ValidationError

class opin(forms.Form):

    titlef = forms.CharField(label='عنوان ',max_length=50, widget=forms.TextInput(attrs={'class':'filed_f','placeholder':'عنوان'}),error_messages={'max_length':'بیشتر از 50 کاراکتر'})
    text_arf = forms.CharField(label='متن',max_length=300, widget=forms.Textarea(attrs={'class':'text_f','placeholder':'متن'}),error_messages={'max_length':'بیشتر از 300 کاراکتر'})



class repo(forms.Form):
    name_f = forms.CharField(max_length=50)
    email_f = forms.CharField()
    text_f = forms.CharField(max_length=300)





