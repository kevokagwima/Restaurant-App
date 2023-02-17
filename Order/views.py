from django.shortcuts import render
from Inventory.models import Category, Item

def home(request):
  categories = Category.objects.all()
  items = Item.objects.all()
  context = {
    'categories': categories,
    'items': items
  }

  return render(request, "order/home.html", context)
