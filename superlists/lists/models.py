from django.db import models
from django.urls import reverse
# Create your models here.

class List(models.Model):

    # metoda pozwala na wskazywanie określonej strony dla elementu
    # zwroci odpowiedni widok adres url dla obiektu modelu (z odpowidnim id)
    # wywolanie redirect na obiektie automatycznie wywoluje get_absolute_url
    def get_absolute_url(self):
        return reverse('lists:view_list', args=[self.id])

# class Item(models.Model):
#     text = models.TextField(default="")
#     list = models.ForeignKey(List, default=None)
#
#     class Meta:
#         unique_together = ('list', 'text') # zapewnienie unikalnosci elementu w liście

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text
