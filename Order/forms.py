from django import forms
from Inventory.models import Item

class NewItemForm(forms.ModelForm):
  class Meta:
    model = Item
    fields = ('category', 'name', 'tag', 'price')

    widgets = {
    'category': forms.Select,
    'name': forms.TextInput,
    'description': forms.Textarea,
    'price': forms.TextInput,
  }
