from django.shortcuts import render, redirect
from .models import Opinion,report
from .forms import opin
from .forms import repo
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

        # check whether it's valid:
        if 'f1' in request.POST:
            form = opin(request.POST)

            if form.is_valid() :
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
        elif 'f2' in request.POST:
            form2 = repo(request.POST)
            if form2.is_valid():
                cont = report (name=form2.cleaned_data.get('name_f'),
                               email=form2.cleaned_data.get('email_f'),
                               text=form2.cleaned_data.get('text_f'),

                               id_c=request.POST['idc']

                               )
                pat = request.POST['path1']
                # redirect to a new URL:
                cont.save()

                return redirect(pat)




    else:
        form = opin()
        form2=repo()
        print(':)')
    ps = product.objects.get(slug=pr)
    op = Opinion.objects.all().order_by('-id')

    return render(request, 'mprodact.html', {'ps': ps, 'form': form, 'op': op,'form2': form2})


def cp(request, ps1, catp):
    c = category.objects.get(slug=catp)
    prs = c.gat.all()
    return render(request, 'catpro.html', {'prs': prs})
