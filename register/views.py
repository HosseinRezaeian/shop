from django.shortcuts import render
from  .form import registerform



def register(request):
    form = registerform()
    if request.method== "POST":
        form=registerform(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = registerform()
    return render(request, 'signup.html', {'form': form})

# Create your views here.
