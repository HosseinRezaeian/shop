from django.http import HttpRequest, HttpResponse, JsonResponse
from products.models import product
from .models import order, order_details
from django.views import View
from django.shortcuts import render, redirect
from register.models import User
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
import jdatetime
from django.contrib.auth.models import User

from django.http import HttpResponse, Http404
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from datetime import date
from .form import profile_change_pass

# Create your views here.
def usercart(request: HttpRequest):
    print(request.GET.get('im'), )
    count = request.GET.get('im')
    producaj = request.GET.get('pro')
    if request.user.is_authenticated:
        prodactmodel = product.objects.filter(id=producaj).first()
        print(request.user.username)
        if prodactmodel is not None:
            print(prodactmodel)
            order_cor, created = order.objects.get_or_create(is_paid=False, user_id=request.user)
            order_cor_ditale = order_cor.order_details_set.filter(product_id=producaj).first()
            if order_cor_ditale is not None:
                order_cor_ditale.countp += int(count)
                order_cor_ditale.save()


            else:
                new_order = order_details(order_id=order_cor.id, product_id=producaj, countp=count)
                new_order.save()

    else:
        print('is not login')
    current_user = request.user
    count_prodact_cart = ''

    if str(current_user) != "AnonymousUser":

        order_v, created = order.objects.get_or_create(is_paid=False, user_id=request.user)
        ps = product.objects.get(title=request.GET.get('np'))

        or_d = order_details.objects.filter(order=order_v, product=ps).first()
        if or_d is not None:
            count_prodact_cart = or_d.countp
        else:
            count_prodact_cart = ''
        return render(request, 'counter.html', {'count_cart': count_prodact_cart})
    return HttpResponse('response')


class cart_shoping(View):
    def get(self, request):
        current_user = request.user

        if str(current_user) != "AnonymousUser":
            mul = 0
            user_open, created = order.objects.get_or_create(is_paid=False, user_id=request.user)
            cart_shop = user_open.order_details_set.all()
            for i in cart_shop:
                mul += i.countp * i.product.price
            print(mul)

            return render(request, 'cart_shoper.html', {'cart_shop': user_open, 'multi': mul})


def shoper_par(request: HttpRequest):
    ditail_id = request.GET.get('ditail_id')
    if ditail_id is None:
        return JsonResponse({'status': 'cant2 found'})
    user_open, created = order.objects.get_or_create(is_paid=False, user_id=request.user)
    ditail_obj = user_open.order_details_set.filter(id=ditail_id).first()
    print(ditail_obj)
    if ditail_obj is None:

        return render(request, 'cart_shop_pa.html', {'cart_shop': user_open})
    else:
        ditail_obj.delete()
        user_open, created = order.objects.get_or_create(is_paid=False, user_id=request.user)
        mul = 0
        cart_shop = user_open.order_details_set.all()
        for i in cart_shop:
            mul += i.countp * i.product.price
    return render(request, 'cart_shop_pa.html', {'cart_shop': user_open, 'multi': mul})

    return HttpResponse('response')


def save_count(request: HttpRequest):
    num = request.GET.get('num')
    id_p = request.GET.get('id_dit')

    if id_p is None:
        return JsonResponse({'status': 'id_p'})
        if num is None:
            return JsonResponse({'status': 'num'})
    ditail = order_details.objects.filter(id=id_p, order__user_id=request.user.id, order__is_paid=False).first()
    print(ditail.product)

    if ditail is None:
        return JsonResponse({'status': 'cant found ditail'})
    ditail.countp = num
    print(ditail.countp)
    ditail.save()
    print(ditail.countp)
    user_open, created = order.objects.get_or_create(is_paid=False, user_id=request.user)
    cart_shop = user_open.order_details_set.all()
    mul = 0
    for i in cart_shop:
        mul += i.countp * i.product.price
    return render(request, 'cart_shop_pa.html', {'cart_shop': user_open, 'multi': mul})



# payment


def go_to_gateway_view(request: HttpRequest):
    user_open, created = order.objects.get_or_create(is_paid=False, user_id=request.user)
    cart_shop = user_open.order_details_set.all()

    current_user = request.user

    if str(current_user) != "AnonymousUser":
        mul = 0
        for i in cart_shop:
            mul += i.countp * i.product.price
        if mul != 0:

            # خواندن مبلغ از هر جایی که مد نظر است
            amount = mul * 10

            # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
            # اختیاری

            factory = bankfactories.BankFactory()
            try:
                bank = factory.create(
                    bank_models.BankType.IDPAY)  # or factory.create(bank_models.BankType.BMI) or set identifier
                bank.set_request(request)
                bank.set_amount(amount)
                # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
                bank.set_client_callback_url(reverse('callback'))
                # اختیاری

                # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
                # پرداخت برقرار کنید.
                bank_record = bank.ready()

                # هدایت کاربر به درگاه بانک
                return bank.redirect_gateway()

            except AZBankGatewaysException as e:
                logging.critical(e)

                raise e


# Create your views here.


def callback_gateway_view(request):
    user_open, created = order.objects.get_or_create(is_paid=False, user_id=request.user)
    cart_shop = user_open.order_details_set.all()
    current_user = request.user
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        hap = 'این لینک معتبر نیست.'
        return render(request, 'callback_is_success.html', {'text': hap})

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        hap = 'این لینک معتبر نیست.'
        return render(request, 'callback_is_success.html', {'text': hap})

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        is_paider = order.objects.get(user_id=current_user, is_paid=0)
        finall_ditail = order_details.objects.filter(final_price=None, order_id=is_paider.id).first()
        finall_ditail2 = order_details.objects.filter(final_price=None, order_id=is_paider.id)
        prodact_all = product.objects.all()

        for dit in finall_ditail2:
            prodact_dit = product.objects.get(id=dit.product_id)
            prodact_dit.number = prodact_dit.number - dit.countp
            dit.final_price = prodact_dit.price

            dit.save()
            prodact_dit.save()




        mul = 0
        for i in cart_shop:
            mul += i.countp * i.product.price
        if mul != 0:
            is_paider.is_paid = True
            today = jdatetime.date.today()
            is_paider.pay_time = str(today)
            is_paider.tracking_code = bank_record.extra_information
            is_paider.final_price = mul

            is_paider.save()

            hap = 'خرید با موفقیت ثبت شد.'

            return render(request, 'callback_is_success.html', {'text': hap})

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    hap = 'پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.'
    return render(request, 'callback_is_success.html', {'text': hap})


class user(View):
    def get(self, request,user_name):
        form = profile_change_pass()
        order_user = order.objects.filter(user_id_id=request.user.id, is_paid=True)
        orm = order_details.objects.filter(order__in=order_user.all())
        oa = []
        for id_e in order_user:
            ore = order_details.objects.filter(order_id=id_e.id)
            if str(ore) == '<QuerySet []>':
                print(str(ore))
            else:
                oa.append([[ore], [id_e.final_price, id_e.pay_time]])
        print(oa)

        # pr = product.objects.all()
        return render(request, 'profile.html', {'order': order_user, 'orm': orm, 'oa': oa,'form':form})


    def post(self, request,user_name):
        User = get_user_model()
        reset_password = profile_change_pass(request.POST)
        user: User = User.objects.filter(username=request.user).first()
        if reset_password.is_valid():
            user: User = User.objects.filter(username__iexact=request.user.username).first()
            if user is None:
                return redirect(reverse('sign'))

            user_pass = reset_password.cleaned_data['password']
            user_pass_con = reset_password.cleaned_data['password_con']
            last_password = reset_password.cleaned_data['last_password']
            is_password_correct = user.check_password(last_password)

            if user_pass == user_pass_con and is_password_correct:
                user.set_password(user_pass)

                user.is_active = True
                user.save()
                print('yes')
                return redirect(reverse('home'))

        context = {
            'resetpass': reset_password
        }

        return render(request, 'reset.html', context)




