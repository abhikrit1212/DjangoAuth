from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'home.html')
        else:
            messages.info(request,'invalid login credentials')
            return render(request,'login.html')
    else:
        if not request.user.is_anonymous:
            return render(request,'home.html')
        else:
            return render(request,'login.html')
def signup(request):
    if request.method=='POST':
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.get(username=request.POST['username'])
                messages.info(request,'Username already taken')
                return render(request,'register.html')
            except User.DoesNotExist:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email=request.POST['email']) 
                return redirect(home) 
        else:
            messages.info(request,'Passwords not matching')
            return render(request,'register.html')
    else:
        if not request.user.is_anonymous:
            return render(request,'home.html')
        else:
            return render(request,'register.html')
@login_required
def logout(request):
    auth.logout(request)
    return redirect(home)