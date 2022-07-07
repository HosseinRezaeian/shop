from django.shortcuts import render

from .models import category
from .models import product


# # Create your views here.
def prodact(request, ps):
    f = category.objects.get(slug=ps)
    g = f.gor.all()

    # c = f.gat.all()

    return render(request, 'pro.html', {'pr': g})


def index(request):
    c = category.objects.all().order_by('id')

    return render(request, 'index.html', {'pr': c})
