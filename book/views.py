from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="/login")
def homeView(request):
    return render(request,'book/home.html')

@login_required(login_url="/login")
def searchView(request):
    data={
        "source" : request.POST['source'],
        "dest" :request.POST['dest']
    }
    return render(request,'book/search.html',data)