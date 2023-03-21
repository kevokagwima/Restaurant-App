from django.urls import path
from . import views

app_name = "Order"

urlpatterns = [
  path("", views.home, name="home"),
  path("home/order/", views.home, name="home"),
  path("loadMenu/", views.loadMenu, name="loadMenu"),
  path("new-order/<str:pk>/", views.newOrder, name="new-order"),
  path("decrease-quantity/<str:pk>/", views.decrease_quantity, name="decrease-quantity"),
  path("remove-item/<int:pk>/", views.removeItem, name="remove-item"),
  path("close-order/<int:pk>/", views.closeOrder, name="close-order"),
  path("card-payment/", views.card_payment, name="card-payment"),
  path("cash-payment/", views.cash_payment, name="cash-payment"),
  path("cash-change/", views.cash_change, name="cash-change"),
  path("success/", views.success, name="success"),
  path("cancel/", views.cancel, name="cancel"),
]
