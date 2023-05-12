from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import random
from django.core.mail import EmailMessage

from .forms import UserProfileForm

def LogoutAccount(request):
    logout(request)
    return redirect('login')


def RegisterAccount(request):
    accounts = User.objects.all()
    context = {
        'accounts': accounts
    }
    return render(request, 'accounts/register.html', context)


def LoginAccount(request):
    if request.method =="POST":
        user = authenticate(request,username=request.POST['username'],password=request.POST['pass'])
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.success(request, "Invalid Username and Password or User does not exist")
    return render(request, "accounts/login.html", {})

def ConfirmAccount(request):
    otp = generateOTP()
    context ={
        'otp':otp,
        'username':request.POST['username'],
        'pass':request.POST['pass'],
        'email':request.POST['email'],
    }
    send_email_otp(request.POST['username'],request.POST['email'],otp)
    return render(request, 'accounts/verify.html', context)

def CreateAccount(request):
    User.objects.create_user(
        username=request.POST['username'], 
        password=request.POST['pass'], 
        email=request.POST['email'])
    
    messages.success(request, f'Account created successfully. Please Log In using that account')
    return redirect('login')

def EditProfile(request):
    userProfile = User.objects.get(id = request.user.id)
    form = UserProfileForm(request.FILES, request.POST)
    if request.method == "POST":
        try:
            userProfile.pfp = request.FILES['pfp']
        except:
            pass
        userProfile.fname = request.POST['fname']
        userProfile.mname = request.POST['mname']
        userProfile.lname = request.POST['lname']
        userProfile.strand = request.POST['strand']
        userProfile.save()
        messages.success(request, 'Profile has been edited')
        return redirect("edit-profile") 
    return render(request, 'accounts/edit_profile.html', {"userProfile":userProfile, "form":form})


def generateOTP():
    return f'{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}'

def send_email_otp(username, email, otp):
    message = f'Good day {username}!,\n\nThis is the OTP for your MapuaMates Account {otp}.\n\nIf this was not requested by you, you can ignore this email.'
    email = EmailMessage(
        'MapuaMates Account OTP',#subject
        message,#message
        to=[email],) #to
    email.fail_silenty=False
    email.send()
