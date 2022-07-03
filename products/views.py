from django.shortcuts import render

from .models import category
from .models import product


# # Create your views here.
def prodact(request, ps):
    f = category.objects.get(slug=ps)
    c = f.category.all()

    return render(request, 'pro.html', {'pr': c})


def index(request):
    c = category.objects.all()

    return render(request, 'index.html', {'pr': c})
