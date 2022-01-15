from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm
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
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_,
                                         'form': form})


# def new_list(request):
#     print(dir(request))
#     list_ = List.objects.create()
#     item = Item(text=request.POST['text'], list=list_)
#     try:
#         item.full_clean() # sprawdzenie poprawności stworzonego obiektu
#         item.save()
#     except ValidationError:
#         list_.delete()
#         error = "Element listy nie może być pusty"
#         return render(request, "home.html", {"error": error})
#     return redirect(list_) # automatycznie wola get_absolute_url


def new_list(request):
    form = ItemForm(data=request.POST) # 
    if form.is_valid(): # 
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form}) # 