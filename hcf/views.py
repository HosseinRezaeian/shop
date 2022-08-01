from django.shortcuts import render
from .models import menu, lep


# Create your views here.
def header(request):
    l = lep.objects.first()
    m = menu.objects.all()

    return render(request, 'header.html', {'menu': m, "lep": l})


def footer(request):
    l = lep.objects.first()

    return render(request, 'footer.html', {"lep": l})
