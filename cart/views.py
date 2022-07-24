from django.http import HttpRequest, HttpResponse, JsonResponse
from products.models import product
from .models import order, order_details
from django.views import View
from django.shortcuts import render


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

        order_v = order.objects.get(user_id=current_user.id)
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
            user_open, created = order.objects.get_or_create(is_paid=False, user_id=request.user)

            return render(request, 'cart_shoper.html', {'cart_shop': user_open})


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
    return render(request, 'cart_shop_pa.html', {'cart_shop': user_open})

    return HttpResponse('response')


def save_count(request: HttpRequest):
    num = request.GET.get('num')
    id_p = request.GET.get('id_p')

    if id_p is None:
        return JsonResponse({'status': 'id_p'})
        if num is None:
            return JsonResponse({'status': 'num'})
    ditail = order_details.objects.filter(id=id_p, order__user_id=request.user.id, order__is_paid=False).first()
    print(ditail)
    if ditail is None:
        return JsonResponse({'status': 'cant found ditail'})
    ditail.countp = num
    ditail.save()
    user_open, created = order.objects.get_or_create(is_paid=False, user_id=request.user)
    return render(request, 'cart_shop_pa.html', {'cart_shop': user_open})
    return HttpResponse('response')
