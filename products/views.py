from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .models import Opinion, report
from cart.models import order, order_details
from .forms import opin
from .forms import repo
from .models import category
from .models import product, discount
from django.contrib.sites.shortcuts import get_current_site


def index(request):
    return render(request, 'list_a.html', {'genres': category.objects.all()})


def home(request):
    prodacts_discounts = product.objects.filter(is_discount=True)
    c = 0
    for i in prodacts_discounts:
        if i.id > c:
            c = i.id
            

    count_discounts = prodacts_discounts.count()
    cat = category.objects.filter(level=0)

    return render(request, 'index.html',
                  {'category': cat, 'prodact_discount': prodacts_discounts, 'count': count_discounts, 'ip': c})


# # Create your views here.
def prodact(request, ps):
    g1 = category.objects.get(id=ps)
    g3 = ps
    g2 = g1.get_children()

    prod = product.objects.all()

    # c = f.gat.all()

    return render(request, 'list_b.html', {'f1': g2, 'g3': g3, 'prod': prod})


def mp(request, catp1, pr):
    if request.method == 'POST':

        print('thank you')
        # create a form instance and populate it with data from the request:

        # check whether it's valid:
        if 'f1' in request.POST:
            form = opin(request.POST)

            if form.is_valid():
                # process the data in form.cleaned_data as required
                cont = Opinion(name=request.POST['namef'],
                               email=request.POST['email_f'],
                               title=form.cleaned_data.get('titlef'),
                               text_area=form.cleaned_data.get('text_arf'),
                               proda=request.POST['prodactf']

                               )
                pat = request.POST['path']
                # redirect to a new URL:
                cont.save()

                return redirect(pat)

            # return redirect('mp')
            print('thanks')
        elif 'f2' in request.POST:
            form2 = repo(request.POST)
            if form2.is_valid():
                cont = report(name=request.POST['name_f'],
                              email=request.POST['email_f'],
                              text=request.POST['text_f'],

                              id_c=request.POST['idc']

                              )
                pat = request.POST['path1']
                # redirect to a new URL:
                cont.save()

                return redirect(pat)





    else:

        form = opin()
        form2 = repo()
        current_user = request.user
        count_prodact_cart = ''

        if str(current_user) != "AnonymousUser":

            order_v, created = order.objects.get_or_create(is_paid=False, user_id=request.user)
            ps = product.objects.get(slug=pr)

            or_d = order_details.objects.filter(order=order_v, product=ps).first()
            if or_d is not None:
                count_prodact_cart = or_d.countp
            else:
                count_prodact_cart = ''

    ps = product.objects.get(slug=pr)
    op = Opinion.objects.filter(proda=ps.id)

    return render(request, 'mprodact.html',
                  {'ps': ps, 'form': form, 'op': op, 'form2': form2, 'count_cart': count_prodact_cart})


def cp(request, ps1, catp):
    c = category.objects.get(slug=catp)
    prs = c.gat.all()
    return render(request, 'catpro.html', {'prs': prs})
