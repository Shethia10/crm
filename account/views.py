from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import CustomUser
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        alt_phone = request.POST['alt_phone']
        designation = request.POST['designation']
        address = request.POST['address']

        if password1 == password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = CustomUser.objects.create_user(username=username, password=password1, email=email, first_name=fname, last_name=lname, phone=phone, alt_phone=alt_phone, designation=designation, address=address)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password did not match')
            return redirect('register')
    else:    
        return render(request, 'account/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')

    else:
        return render(request, 'account/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')