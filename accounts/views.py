from django.contrib import messages, auth
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from contacts.models import Contact


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name',False)
        last_name = request.POST.get('last_name',False)
        username = request.POST.get('username',False)
        email = request.POST.get('email',False)
        password = request.POST.get('password',False)
        password2 = request.POST.get('password2',False)
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, first_name=first_name,password=password,email=email ,
                                                    last_name=last_name)
                    user.save()
                    messages.success(request,'You are now registered and can log in')
                    return redirect('login')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'something get wrong')
    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are now logged out' )
        return redirect('index')
    return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts':user_contacts,
    }
    return render(request, 'accounts/dashboard.html',context)