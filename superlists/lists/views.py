from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List
from django.core.exceptions import ValidationError

# Create your views here.


# def home_page(request):
#     if request.method == 'POST':
#         new_item_text = request.POST['item_text']
#         Item.objects.create(text=new_item_text)
#     else:
#         new_item_text=""

#     return render(request, 'home.html', {
#         'new_item_text': new_item_text,
#     }) #D jango automatycznie szuka katalogow templates szuka pliku html i tworzony jest http request

def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error=None
    if request.method == "POST":
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "Element nie może być pusty"
    return render(request, 'list.html', {'list': list_,
                                         'error': error})


def new_list(request):
    print(dir(request))
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean() # sprawdzenie poprawności stworzonego obiektu
        item.save()
    except ValidationError:
        list_.delete()
        error = "Element nie może być pusty"
        return render(request, "home.html", {"error": error})
    return redirect(list_) # automatycznie wola get_absolute_url


