from django.shortcuts import render
from Inventory.models import Category, Item, User_Profile
from django.contrib.auth.models import User

def home(request):
  categories = Category.objects.all()
  items = Item.objects.all()
  user = request.user
  user_profile = User_Profile.objects.filter(user=request.user).first()
  context = {
    'categories': categories,
    'items': items,
    'user': user,
    'user_profile': user_profile
  }

  return render(request, "order/home.html", context)
