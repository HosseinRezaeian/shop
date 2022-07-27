from django.http import HttpRequest, HttpResponse, JsonResponse
from products.models import product
from .models import order, order_details
from django.views import View
from django.shortcuts import render, redirect
import logging
from django.http import HttpResponse, Http404
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from datetime import date


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
    return HttpResponse('response')


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
            amount = mul

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
                # TODO: redirect to failed page.
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
        return render(request, 'callback_isnot_success.html', {'text': hap})

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        hap = 'این لینک معتبر نیست.'
        return render(request, 'callback_isnot_success.html', {'text': hap})

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        is_paider = order.objects.get(user_id=current_user, is_paid=0)
        finall_ditail = order_details.objects.filter(final_price=None, order_id=is_paider.id).first()

        mul = 0
        for i in cart_shop:
            mul += i.countp * i.product.price
        if mul != 0:
            is_paider.is_paid = True
            today = date.today()
            is_paider.pay_time = today
            finall_ditail.final_price = mul
            finall_ditail.save()
            is_paider.save()
            hap='پرداخت با موفقیت انجام شد.'
            return render(request, 'callback_isnot_success.html',{'text':hap})


    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    hap = 'پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.'
    return render(request, 'callback_isnot_success.html', {'text': hap})
