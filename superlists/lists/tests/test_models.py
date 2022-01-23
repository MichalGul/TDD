from django.test import TestCase
from ..models import Item, List
from django.core.exceptions import ValidationError
# Create your tests here.


class ItemModelTest(TestCase):

    # def test_saving_and_retrieving_items(self):
    #
    #     list_ = List()
    #     list_.save()
    #
    #     first_item = Item()
    #     first_item.text = "Absolutnie pierwszy element listy"
    #     first_item.list=list_
    #     first_item.save()
    #
    #     secon_item = Item()
    #     secon_item.text = "Drugi element"
    #     secon_item.list=list_
    #     secon_item.save()
    #
    #     saved_list = List.objects.first()
    #     self.assertEqual(saved_list, list_)
    #
    #     saved_items = Item.objects.all()
    #     self.assertEqual(saved_items.count(), 2)
    #
    #     first_saved_item = saved_items[0]
    #     second_saved_item = saved_items[1]
    #     self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element listy')
    #     self.assertEqual(first_saved_item.list, list_)
    #     self.assertEqual(second_saved_item.text, 'Drugi element')
    #     self.assertEqual(second_saved_item.list, list_)

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, "")

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()


    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # Nie powinien być zgłoszony.


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        print(list_.get_absolute_url())  # returns /lists/1/
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
