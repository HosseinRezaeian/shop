from django.shortcuts import render, redirect
from .models import Opinion
from .forms import opin
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


def mp(request, catp1, pr, p):
    if request.method == 'POST':
        print('thank you')
        # create a form instance and populate it with data from the request:
        form = opin(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            cont = Opinion(name=form.cleaned_data.get('namef'),
                           email=form.cleaned_data.get('emailf'),
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

        # if a GET (or any other method) we'll create a blank form
    else:
        form = opin()
        print(':)')
    ps = product.objects.get(slug=pr)
    op = Opinion.objects.all().order_by('-id')

    return render(request, 'mprodact.html', {'ps': ps, 'form': form, 'op': op})


def cp(request, ps1, catp):
    c = category.objects.get(slug=catp)
    prs = c.gat.all()
    return render(request, 'catpro.html', {'prs': prs})
