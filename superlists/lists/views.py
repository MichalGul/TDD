from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home_page(request):
    return render(request, "home.html") #Django automatycznie szuka katalogow templates szuka pliku html i tworzony jest http request
