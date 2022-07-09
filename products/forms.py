from django import forms


class opin(forms.Form):
    namef = forms.CharField(label='نام  و نام خانوادگی',max_length=50, widget=forms.TextInput,error_messages={'max_length':'بیشتر از 50 کاراکتر'})
    emailf = forms.CharField(label='ایمیل', widget=forms.EmailInput,error_messages={'max_length':'بیشتر از 50 کاراکتر'})
    titlef = forms.CharField(label='عنوان ',max_length=50, widget=forms.TextInput,error_messages={'max_length':'بیشتر از 50 کاراکتر'})
    text_arf = forms.CharField(label='متن',max_length=300, widget=forms.Textarea,error_messages={'max_length':'بیشتر از 300 کاراکتر'})



