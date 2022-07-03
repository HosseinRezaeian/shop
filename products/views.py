from django.shortcuts import render

from .models import product


# Create your views here.
def index(request):
    c = product.objects.all()

    return render(request, 'index.html', {'pr': c})
