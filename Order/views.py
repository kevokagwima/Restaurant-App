from django.shortcuts import render, redirect
from Inventory.models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
import random

def home(request):
  categories = Category.objects.all().exclude(title=["Meals", "Sides"])
  meal_category = Category.objects.filter(title="Meals").first()
  side_category = Category.objects.filter(title="Sides").first()
  items = Item.objects.all()
  meals = Meals.objects.all()
  sides = Sides.objects.all()
  user = request.user
  user_profile = User_Profile.objects.filter(user=request.user).first()
  active_order = Order.objects.filter(is_active=True).first()
  order_items = OrderItems.objects.filter(order=active_order).all()
  context = {
    'categories': categories,
    'meal_category': meal_category,
    'side_category': side_category,
    'items': items,
    'meals': meals,
    'sides': sides,
    'user': user,
    'user_profile': user_profile,
    'active_order': active_order,
    'order_items': order_items
  }

  return render(request, "order/home.html", context)

def loadMenu(request):
  categories = Category.objects.all()
  meal_category = Category.objects.filter(title="Meals").all()
  side_category = Category.objects.filter(title="Sides").all()
  meals = Meals.objects.all()
  sides = Sides.objects.all()
  items = Item.objects.all()
  return JsonResponse(
    {
      "categories": list(categories.values()),
      "meal_category": serializers.serialize("json", meal_category),
      "side_category": serializers.serialize("json", side_category),
      "meals": list(meals.values()),
      "sides": list(sides.values()),
      "items": list(items.values())
    }
  )

def newOrder(request, pk):
  active_order = Order.objects.filter(is_active=True).first()
  if active_order:
    meal = Meals.objects.get(name=pk)
    if meal:
      order_item = OrderItems.objects.filter(item_name=pk).first()
      if order_item:
        order_item.item_quantity = order_item.item_quantity + 1
        order_item.save()
        messages.success(request, "Cart updated successfully")
      else:
        new_order_item = OrderItems.objects.create(
          order = active_order,
          unique_id = random.randint(100000,999999),
          item_name = meal.name,
          item_price = int(meal.price)
        )
        new_order_item.save()
        messages.success(request, "Item added to cart")
      return redirect('Order:home')
    else:
      messages.error(request, "Item not found")
      return redirect('Order:home')
  else:
    new_order = Order.objects.create()
    new_order.save()
    new_order_item = OrderItems.objects.create(
      order = new_order,
      unique_id = random.randint(100000,999999),
      item_name = meal.name,
      item_price = int(meal.price)
    )
    new_order_item.save()
    messages.success(request, "A new order has been created")

  return redirect('Order:home')

def removeItem(request, pk):
  try:
    order_item = OrderItems.objects.get(unique_id=pk)
    if order_item:
      order_item.delete()
      messages.success(request, "Order item removed")
    else:
      messages.error(request, "Order item not found")
  except:
    messages.error(request, "An error occured")

  return redirect("Order:home")
