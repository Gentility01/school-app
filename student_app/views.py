from django.contrib.auth import login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages

from student_app.EmailBackEnd import EmailBackEnd

# Create your views here.
def showDemoPage(request):
    return render(request, 'student_app/demo.html')


def ShowLoginPage(request):
    return render(request, 'student_app/login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>This method is not allowed </h2>")

# here we use the name given to our html input form to access the values  on submitting  Values 
# if method  is post here (else condition ) then i will proccess the form
# note we will create an EmailBackend after here
    else:
        # now creating  user object by calling  Method EmailBackend.authenticate() and passing  Email and Password
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))   
        # if user is not None then i will call the login() method and passing  UserObject
        if user != None: 
            # calling the  login method and passing  User Object
            login(request, user)
            # return HttpResponse("Email : "+request.POST.get("email") +" Password :"+request.POST.get("password"))

            # lets proccess login for diffrent users (HOD, Staffs, Students)
            if user.user_type =="1":  #remeber user_type is from models.py(line 17)
                return HttpResponseRedirect('/admin_home')
            elif user.user_type =="2":
                return HttpResponse("Staff login")
            else:
                return HttpResponse("Student login")


            return HttpResponseRedirect('/admin_home')   # now the login need to redirect to our HODpage
            # else i will return the invalid login  message
        else:
            messages.error(request, 'Invalid Login Details')
            return HttpResponseRedirect('login/')

# note go to the urls and create the routes for get user details and also for logout
def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User :"+request.user.email + "usertype :"+request.user.user_type)
    else:
        return  HttpResponse('please login first')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('login/')

 



