from django.urls import path
from django.contrib.auth import views as ath_views
from . import views
from .forms import User_Login_Form

app_name = 'Core'

urlpatterns = [
  path("login/", ath_views.LoginView.as_view(template_name='core/login.html', authentication_form=User_Login_Form), name="login"),
  path("logout/", views.logout_user, name="logout")
]
