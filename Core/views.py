from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import User_Login_Form

def login(request):
  form = User_Login_Form()
  if form.is_valid():
    messages.success(request, "Login successfull")
  context = {
    'form': form
  }
  return render(request, "core/login.html", context)

@login_required(login_url='/login')
def logout_user(request):
  logout(request)
  messages.success(request, "Logout successfull")
  return redirect('Core:login')
