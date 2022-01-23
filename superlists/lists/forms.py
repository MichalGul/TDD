from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError

#
# class ItemForm(forms.Form):
#     item_text = forms.CharField(
#         widget=forms.fields.TextInput(attrs={ # dodanie widgetu podpwiedzi do formularza, co sprowadza sie do dodatnia adtybutów do htmla
#             'placeholder': "Wpisz rzecz do zrobienia",
#             'class': "form-control input-lg"
#         })
#     )

EMPTY_LIST_ERROR = "Element listy nie może być pusty"
DUPLICATE_ITEM_ERROR = "Podany element już istnieje na liście."


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

    def save(self, for_list):
        # instance przedstawia modyfikowany lub tworzony obiekt bazy danych
        self.instance.list = for_list
        return super().save() # zapisuje dane z formularza do bazy danych




class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)


