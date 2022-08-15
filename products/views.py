from django.http import HttpResponse, HttpRequest
from django.db.models import Avg, Max, Min
from django.shortcuts import render, redirect
from .models import Opinion, report
from cart.models import order, order_details
from .forms import opin
from .forms import repo
from .models import category
from django.views.generic import ListView
from .models import product, discount
from django.contrib.sites.shortcuts import get_current_site


# category all
def index(request):
    return render(request, 'list_a.html', {'genres': category.objects.all()})


# home
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


list_p = []


#
# next category
# def prodact(request, ps):
#     global list_p
#     g1 = category.objects.get(id=ps)
#
#     g3 = ps
#
#     g2 = g1.get_children()
#     sub_menu(g2)
#     list_product = list_p
#     list_p = []
#     for i in list_product:
#         i1 = str(i)
#         if i1 == '<QuerySet []>':
#             list_product.remove(i)
#
#     prod = product.objects.all()
#
#     return render(request, 'list_b.html', {'f1': g2, 'g3': g3, 'prod': prod,
#                                            'list_product': list_product})


class prodact_list_view(ListView):
    template_name = 'testlistview.html'
    paginate_by = 2


    context_object_name = 'list_product'

    def get_queryset(self, *args, **kwargs):

        global categoryForsend
        global list_p
        global categoryKey

        categoryKey = category.objects.get(id=self.kwargs['ps'])
        categoryForsend = categoryKey.get_children()

        sub_menu(categoryForsend)
        list_product = list_p
        list_p = []
        for i in list_product:
            i1 = str(i)
            if i1 == '<QuerySet []>':
                list_product.remove(i)

        prod = product.objects.all()

        list_test = []
        for listQuery in list_product:
            for pr in listQuery:
                list_test.append(pr)

        for ted in prod:
            if ted.category1_id == int(self.kwargs['ps']):


                list_test.append(ted)
        print(list_test)

        return list_test

    def get_context_data(self, *args, **kwargs):
        context = super(prodact_list_view, self).get_context_data(*args, **kwargs)

        context['categorySend'] = categoryForsend

        return context

    #


def sub_menu(c2):
    global list_p

    for item in c2:
        product_filter = product.objects.filter(category1_id=item.id)
        if str(item.get_children()) is not '<QuerySet []>':
            list_p.append(product_filter)

        if str(item.get_children()) != '<TreeQuerySet []>':
            sub_menu(item.get_children())


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
                               proda=request.POST['prodactf'],
                               answer_id=request.POST.get('answer', None)

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
    op = Opinion.objects.filter(proda=ps.id).order_by('-id')

    return render(request, 'mprodact.html',
                  {'ps': ps, 'form': form, 'op': op, 'form2': form2, 'count_cart': count_prodact_cart})


def cp(request, ps1, catp):
    c = category.objects.get(slug=catp)
    prs = c.gat.all()
    return render(request, 'catpro.html', {'prs': prs})
