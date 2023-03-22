from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Inventory.models import *
from .forms import NewItemForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.conf import settings
import random, stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='/login')
def home(request):
  categories = Category.objects.all().exclude(title=["Meals", "Sides"])
  meal_category = Category.objects.filter(title="Meals").first()
  side_category = Category.objects.filter(title="Sides").first()
  items = Item.objects.all()
  meals = Meals.objects.all()
  sides = Sides.objects.all()
  all_items = []
  for item,side,meal in zip(items,sides,meals):
    all_items.append(item)
    all_items.append(side)
    all_items.append(meal)
  orders = Order.objects.all()
  all_order_items = OrderItems.objects.all()
  user = request.user
  user_profile = User_Profile.objects.filter(user=request.user).first()
  active_order = Order.objects.filter(is_active=True).first()
  order_items = OrderItems.objects.filter(order=active_order).all()
  total = []
  for order_item in order_items:
    total.append(order_item.item_price*order_item.item_quantity)
  tax = (10*sum(total))/100
  if active_order:
    active_order.total = sum(total)
    active_order.save()
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
    'order_items': order_items,
    'total': sum(total),
    'tax': int(tax),
    'orders': orders,
    'all_order_items': all_order_items,
    'form': NewItemForm(),
    'all_items': all_items
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
  meal = Meals.objects.filter(name=pk).first() or Sides.objects.filter(name=pk).first() or Item.objects.filter(name=pk).first()
  if active_order:
    if meal:
      order_item = OrderItems.objects.filter(item_name=pk, order=active_order).first()
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
    new_order = Order.objects.create(
      order_no=random.randint(100000,999999)
    )
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

def decrease_quantity(request, pk):
  active_order = Order.objects.filter(is_active=True).first()
  if active_order:
    order_item = OrderItems.objects.filter(item_name=pk, order=active_order).first()
    if order_item and order_item.item_quantity >= 2:
      order_item.item_quantity = order_item.item_quantity - 1
      order_item.save()
    else:
      order_item.delete()
    messages.success(request, "Cart updated successfully")
  else:
    messages.error(request, "An error occured")
  
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

def closeOrder(request, pk):
  try:
    active_order = Order.objects.filter(order_no=pk, is_active=True).first()
    if active_order:
      active_order.is_active = False
      active_order.save()
      messages.success(request, "Order has been canceled")
    else:
      messages.error(request, "Order not found")
  except:
    messages.error(request, "An error occured")

  return redirect("Order:home")

  def post(self, request, *args, **kwargs):
    YOUR_DOMAIN = "http://127.0.0.1:8000"
    checkout_session = stripe.checkout.Session.create(
      line_items = [
        {
          'price': '{{PRICE_ID}}',
          'quantity': 1,
        },
      ],
      mode = 'payment',
      success_url = YOUR_DOMAIN + '/success/',
      cancel_url = YOUR_DOMAIN + '/cancel/',
    )
    return JsonResponse({
      'id': checkout_session.id
    })

def card_payment(request):
  try:
    YOUR_DOMAIN = "http://127.0.0.1:8000/"
    active_order = Order.objects.filter(is_active=True).first()
    if active_order.total < 50:
      messages.warning(request, "Orders less than ksh 50 are paid via cash")
      return redirect("Order:home")
    checkout_session = stripe.checkout.Session.create(
      line_items = [
        {
          'price_data': {
            'currency': 'KES',
            'product_data': {
              'name': f'Order #{active_order.order_no}',
            },
            'unit_amount': (active_order.total * 100),
          },
          'quantity': 1,
        }
      ],
      mode = 'payment',
      success_url = YOUR_DOMAIN + 'success/',
      cancel_url = YOUR_DOMAIN + 'cancel/',
    )
    return redirect(checkout_session.url)
  except:
    messages.error(request, "Payment could not be processed")
    return redirect('Order:home')

def cash_payment(request):
  active_order = Order.objects.filter(is_active=True).first()
  context = {
    'active_order': active_order
  }
  if request.method == "POST":
    amount = request.POST["cash-paid"]
    request.session["cash-paid"] = amount
    if int(amount) < active_order.total:
      messages.error(request, "The cash paid is less than the order total")
    elif int(amount) == active_order.total:
      return redirect('Order:success')
    elif int(amount) > active_order.total:
      messages.info(request, "Calculating the change")
      return redirect('Order:cash-change')
  return render(request, "Order/cash.html", context)

def cash_change(request):
  active_order = Order.objects.filter(is_active=True).first()
  cash_paid = request.session["cash-paid"]
  change = int(cash_paid) - active_order.total
  context = {
    'active_order': active_order,
    'change': change
  }

  return render(request, "Order/change.html", context)

def success(request):
  active_order = Order.objects.filter(is_active=True).first()
  active_order.is_active = False
  active_order.save()
  messages.success(request, "Payment was successfull")
  return redirect('Order:home')

def cancel(request):
  messages.error(request, "Payment could not be processed")
  return redirect('Order:home')
