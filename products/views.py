from django.shortcuts import render

from .models import category
from .models import product


def index(request):
    c = category.objects.all().order_by('id')

    return render(request, 'index.html', {'pr': c})


# # Create your views here.
def prodact(request, ps):
    f = category.objects.get(slug=ps)
    g = f.gor.all()
    prod = product.objects.all()

    # c = f.gat.all()

    return render(request, 'list_b.html', {'f': g, 'prod': prod})


def mp(request, catp1,pr,p):
    ps = product.objects.get(slug=pr)
    return render(request, 'mprodact.html', {'ps': ps})


def cp(request, ps1, catp):


    c = category.objects.get(slug=catp)
    prs = c.gat.all()
    return render(request, 'catpro.html', {'prs': prs})
