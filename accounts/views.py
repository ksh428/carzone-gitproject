from django.shortcuts import redirect, render
from django.contrib import messages,auth
from django.contrib.auth.models import User

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Wrong email/password')
            return redirect('login')


    return render(request,'accounts/login.html')

def register(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exists. Use a different username')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'email already exists')
                    return redirect('register')
                else:
                    user=User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=username,password=password)
                    auth.login(request,user) #automatically login the current user
                    messages.success(request,'logged in')
                    return redirect('dashboard')
                    user.save()
                    messages.success(request,'User successfully registered')
                    return redirect('login')

        
        else:
            messages.error(request,'Passwords do not match')
            return redirect('register')
            

    else:
        return render(request,'accounts/register.html')
    

def dashboard(request):
    return render(request,'accounts/dashboard.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        messages.success(request,'logged out')
        return redirect('home')
        

    return redirect('home')