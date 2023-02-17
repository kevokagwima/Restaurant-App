from django.urls import path
from . import views

app_name = "Order"

urlpatterns = [
  path("home/", views.home, name="home"),
]
