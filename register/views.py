from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views import View
from .form import regisform, loginform, forgetform, resetform
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from utils.email_servis import send_email


class registerV(View):
    def get(self, request):
        form = regisform()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = regisform(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_password = form.cleaned_data['password']
            user_conpassword = form.cleaned_data['password_con']
            user_name = form.cleaned_data['username']
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            user1: bool = User.objects.filter(username__iexact=user_name).exists()
            if user:

                form.add_error('', 'تکراری email')
            elif user1:
                form.add_error('', 'تکراری username ')
            elif user_conpassword == user_password:
                new_user = User(email=user_email,
                                email_active_code=get_random_string(72),
                                username=user_name,
                                is_active=False)
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'email1.html')
                return redirect(reverse('login'))
            else:
                form.add_error('', ' مغایرت دارد ')

        return render(request, 'signup.html', {'form': form})


class activate(View):
    def get(self, request, code):
        user = User.objects.filter(email_active_code__iexact=code).first()
        if user is not None:
            print(user, code)
            user.is_active = True
            user.email_active_code = get_random_string(72)
            user.save()
            return redirect(reverse('login'))


class loginV(View):
    def get(self, request):
        login_form = loginform()
        context = {
            'login_form': login_form
        }

        return render(request, 'login.html', context)

    def post(self, request: HttpRequest):
        login_form = loginform(request.POST)
        if login_form.is_valid():
            cap = login_form.cleaned_data.get('captcha')
            print(cap)
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user and cap is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect('index')
                    else:
                        login_form.add_error('email', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')

        else:
            login_form.add_error('captcha', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }

        return render(request, 'login.html', context)


class forgetV(View):
    def get(self, request):
        forget_form = forgetform()
        context = {
            'forget_form': forget_form
        }

        return render(request, 'forget.html', context)

    def post(self, request):
        forget_form = forgetform(request.POST)
        if forget_form.is_valid():
            user_email = forget_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('فعالسازی حساب کاربری', user.email, {'user': user}, 'forgetpas1.html')
                return redirect(reverse('login'))
        context = {
            'forget_form': forget_form
        }

        return render(request, 'forget.html', context)


class resetV(View):
    def get(self, request, code):
        user: User = User.objects.filter(email_active_code__iexact=code).first()
        if user is None:
            return redirect(reverse('login'))
        reset_password = resetform()
        print(user)

        context = {
            'resetpass': reset_password
        }

        return render(request, 'reset.html', context)

    def post(self, request, code):
        reset_password = resetform(request.POST)
        if reset_password.is_valid():
            user: User = User.objects.filter(email_active_code__iexact=code).first()
            if user is None:
                return redirect(reverse('sign'))
            user_pass = reset_password.cleaned_data['password']
            user.set_password(user_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login'))

        context = {
            'resetpass': reset_password
        }

        return render(request, 'reset.html', context)


# Create your views here.
class LogoutV(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login'))
