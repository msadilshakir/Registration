from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from urllib.parse import urlparse
import sys
from flask import jsonify
from django.http import HttpResponse
import socket, ssl , smtplib

# Create your views here.




def home(request):
        return render(request,'home.html')

 
def register(request):

        if request.method == 'POST':
                
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                username = request.POST['username']
                email = request.POST['email']
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                #return HttpResponse(cartype)
                if first_name == '':
                        messages.error(request, 'Please Enter First name')
                elif last_name == '':
                        messages.error(request, 'Please Enter Last name')
                elif username == '':
                        messages.error(request, 'Please Enter username')
                elif User.objects.filter(username=username).exists():
                        messages.error(request, 'Username Already Exists')
                elif email == '':
                        messages.error(request, 'Please Enter email')
                elif User.objects.filter(email=email).exists():
                        messages.error(request, 'Email Address Already Exists!')
                elif password1 == '':
                        messages.error(request, 'Please Enter Password')
                elif password2 == '':
                        messages.error(request, 'Please Re-enter Password')
                elif password1 == password2:
                        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name= last_name)
                        user.save()
                        messages.error(request, 'User Created')
                        #print("User Created")

                        
                showurlpath1 = request.path
                return render(request, 'registration.html', {'path_display': showurlpath1, 'post_value': request.POST})

        return render(request, 'registration.html')


def login(request):
        if request.method == 'POST':
                #return HttpResponse(request.POST.items())
                username = request.POST['username']
                password1 = request.POST['password1']
                user = auth.authenticate(username=username,password=password1)
                if user is not None:
                        auth.login(request,user)
                        messages.error(request, 'Successfully Logged IN')
                        return redirect('/dashboard')
                else:   
                        return redirect('/')
                        messages.error(request,'Invalid Credentials!!!')
        return render(request, 'home.html')        #return redirect('/login')

def logout(request):
        auth.logout(request)
        return redirect('/')

def dashboard(request):
        if request.user.is_authenticated:
                return render(request, 'dyanamic_user.html')
        else:
                return render(request, 'home.html')

def register1(request):
        if request.user.is_authenticated:
                auth.logout(request)
        return redirect('/register')

def forgetpass(request):
        if request.method == 'POST':
                email=request.POST['email']
                if User.objects.filter(email=email).exists():
                        sender_mail="worpdressdeveloper1990@gmail.com"
                        recieve_mail=email
                        password='Test@123'
                        context=ssl.create_default_context()

                        try:
                                s=smtplib.SMTP("smtp.gmail.com",587)
                                s.ehlo()
                                s.starttls(context=context)
                                s.ehlo()
                                s.login(sender_mail,password)
                                message=password
                                s.sendmail(sender_mail,recieve_mail,message)
                                messages.error(request,'Email has been Sent To Your Registered Email ID!!')
                        except Exception as ex:
                               messages.error(request,ex)
                               print(ex)
                        finally:
                                s.quit()
                        return render(request,'forgetpass.html',{'email':email,'s':s})
                else:
                        messages.error(request,'Email Does Not Exist')
                                
        return render(request,'forgetpass.html')

def show(request):
        user_fetch=User.objects.all()
        return render(request,'show.html',{'userft':user_fetch})

def reset(request):
        return render(request,'reset.html')