from django.urls import path
from . import views
app_name = "Inventory"

urlpatterns = [
  path("Inventory/", views.home, name="home"),
]
