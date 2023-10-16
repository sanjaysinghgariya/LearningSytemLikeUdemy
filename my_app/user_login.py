from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from my_app.EmailBackend import EmailBackEnd


def Register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(username, email, password)
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email Already exist please try to login')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username Already exist please try another')
            return redirect('register')
        
        user = User(
            username = username,
            email= email
        )
        user.set_password(password)
        user.save()
        return redirect('login')


    return render(request, 'registration/register.html')


def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = EmailBackEnd.authenticate(request, username=email, password=password)
        if user != None:
            login(request,user)
            messages.success(request, 'Login success')
            return redirect('Home')
        else:
            messages.error(request, 'Email and Password are inValid')
            return redirect('login')


    return render(request, 'registration/login.html')

def Profile(request):
    pk = request.user.id 
    user = User.objects.get(id=pk)
    context = {
        'user' : user
    }
    return  render(request, 'registration/profile.html', context)

def Profile_Update(request):
    pk = request.user.id 
    user = User.objects.get(id=pk)
    context = {
        'user' : user
    }
    print('request.method', request.method)
    if request.method == "POST":
        print('hello yaha par hu ')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('username')
        password = request.POST.get('username')
        user_id = request.user.id
        print(user.email)

        user = User.objects.get(id=user_id)
        
        if first_name != None and first_name != '':
            user.first_name = first_name
        if last_name != None and last_name != '':
            user.last_name = last_name
        if email != None and email != '':
            user.email = email
        if username != None and username != '':
            user.username = username
        
        if password!= None and password != '':
            user.set_password(password)
        user.save()
        print(user.email)
        messages.success(request, 'Profile Are Successfully Updated')
        return redirect('profile')
    
    return  render(request, 'registration/profileupdate.html', context)
