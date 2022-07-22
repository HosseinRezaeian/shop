from django.http import HttpRequest, HttpResponse
from products.models import product
from .models import order, order_details


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
    return HttpResponse('hello')

