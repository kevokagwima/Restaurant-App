from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import User_Profile, Item, Category, Brand

@login_required(login_url='/login')
def home(request):
  user_profile = User_Profile.objects.filter(user=request.user).first()
  items = Item.objects.all()
  user_profiles = User_Profile.objects.all()
  categories = Category.objects.all()
  brands = Brand.objects.all()
  users = User.objects.all().exclude(username="Admin")
  context = {
    'user_profile': user_profile,
    'items': items,
    'categories': categories,
    'brands': brands,
    'users': users,
    'user_profiles': user_profiles
  }

  return render(request, "inventory/home.html", context)
