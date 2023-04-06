from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.template import loader
import pandas as pd
import datetime
from server.views import dataEditer
template = loader.get_template('Message.html')
# Create your views here.


@login_required(login_url='login')
# @api_view(['PUT'])
def HomePage(request):
    if (request.method == 'POST'):
        try:
            my_uploaded_file = request.FILES['my_uploaded_file']
            df = pd.read_csv(my_uploaded_file)
            dataEditer(df)
        except:
            context = {
                'message': "Invalid Data File 😢",
            }
            return HttpResponse(template.render(context, request))

    return render(request, 'home.html')


def SignupPage(request):
    if request.method == 'POST':
        try:
            uname = request.POST.get('username')
            email = request.POST.get('email')
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')

            if pass1 != pass2:
                context = {
                    'message': "Your password and confirm password are not Same!!",
                }
                return HttpResponse(template.render(context, request))
            else:

                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                return redirect('login')
        except:
            context = {
                'message': "Something went Wrong 🤔 Try Again 👍",
            }
            return HttpResponse(template.render(context, request))

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            pass1 = request.POST.get('pass')
            user = authenticate(request, username=username, password=pass1)
            if user is not None:
                login(request, user)
                with open('user\LogFiles\Entry.txt', 'a') as f:
                    f.write(f'{user},{datetime.datetime.now()}\n')
                    f.close()
                return redirect('home')
            else:
                context = {
                    'message': "Username or Password is incorrect!!!",
                }
                return HttpResponse(template.render(context, request))
        except:
            context = {
                'message': "Something went Wrong 🤔 Try Again 👍",
            }
            return HttpResponse(template.render(context, request))
    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')
