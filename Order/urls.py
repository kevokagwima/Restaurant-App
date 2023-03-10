from django.urls import path
from . import views

app_name = "Order"

urlpatterns = [
  path("home/", views.home, name="home"),
  path("loadMenu/", views.loadMenu, name="loadMenu"),
  path("new-order/<str:pk>/", views.newOrder, name="new-order"),
  path("remove-item/<int:pk>/", views.removeItem, name="remove-item"),
]
