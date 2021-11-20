from django import forms
from lists.models import Item
#
# class ItemForm(forms.Form):
#     item_text = forms.CharField(
#         widget=forms.fields.TextInput(attrs={ # dodanie widgetu podpwiedzi do formularza, co sprowadza sie do dodatnia adtybutów do htmla
#             'placeholder': "Wpisz rzecz do zrobienia",
#             'class': "form-control input-lg"
#         })
#     )

EMPTY_LIST_ERROR = "Element listy nie może być pusty"

class ItemForm(forms.models.ModelForm):
    class Meta:
        model=Item # model dla ktorego jest przeznaczony formularz
        fields = ('text',) # pole do użycia
        widgets = { #dodanie atrybutow do html
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Wpisz rzecz do zrobienia',
                'class': 'form-control input-lg',
                }),
        }
        error_messages= {
            'text': {'required': EMPTY_LIST_ERROR}
        }