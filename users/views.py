from .models import User
from .forms import LoginForm
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

class LoginView(View):
    def get(self,request):
        form = LoginForm()
        return render(request,'login.html',{"form":form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return render(request,'login.html',{"form":form,"msg":"Akaunt topilmadi"})
        else:
            return render(request,'login.html',{"form":form,"msg":"Kataklarni to‘g‘ri to‘ldiring"})
        return render(request,'login.html',{"form":form})
    

def logout_web(request):
    logout(request)
    return redirect('home')
        
                
