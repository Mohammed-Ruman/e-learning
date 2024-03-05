
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from account.email import send_otp_via_email,send_otp
from django.urls import reverse
import random
from django.contrib.auth.decorators import login_required



User=get_user_model()


# Create your views here.
@login_required(login_url="login/")
def home_page(request):
    email=request.user
    user=User.objects.get(email=email)
    full_name=user.name()
    return render(request,'index.html',{'name':full_name})


def register_page(request):
    if request.method != 'POST':
        return render(request,'register.html')
    data=request.POST
    email=data.get('email')
    first_name=data.get('first_name')
    last_name=data.get('last_name')
    password=data.get('password')
    registration_type = request.POST.get('registrationType')

    user=User.objects.filter(email=email)

    if user.exists():
        if user.first().is_verified:
            messages.info(request, "Email Already Exists")
            return redirect('register')
        else:
            send_otp_via_email(email)
            return redirect(reverse('verify', args=[email]))


    user=User.objects.create(
        email=email,
        first_name=first_name,
        last_name=last_name  
        )

    if registration_type=='teacher':
        user.is_teacher=True

    user.set_password(password)
    user.save()
    messages.success(request, "Registration Successfully! Check Email for Account Activation")
    send_otp_via_email(email)
    return redirect(reverse('verify', args=[email]))

def logout_page(request):
    logout(request)
    return redirect('login')

def verify_otp(request,email):
    user = get_object_or_404(User, email=email)
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if user.otp == otp:
            # OTP is verified, mark user as verified
            user.is_verified = True
            user.save()
            messages.success(request, "Email Verified Successfully!")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    
    return render(request, 'verify.html', {'email': email})


def login_page(request):
    if request.method != 'POST':
        return render(request,'login.html')

    data=request.POST
    email=data.get('email')
    password=data.get('password')
    user_obj=User.objects.filter(email=email)
    if not user_obj.exists():
        messages.info(request, "Invalid Email")
        return redirect('login')

    user = authenticate(email=email, password=password)
    print(f"Auth User: {user}")

    if user is not None:
        
        if user.is_verified:
            otp=random.randint(100000,999999)
            send_otp(otp,email)
            user.otp=otp
            user.save()
            return redirect(reverse('verify_login', args=[email]))
        messages.info(request, "Account is not activated. Kindly Verify your email")
        send_otp_via_email(email)
        return redirect(reverse('verify', args=[email]))
    else:
        messages.info(request, "Wrong Password")
        return redirect('login')
    

def verify_otp_login(request,email):

    user = get_object_or_404(User, email=email)

    print(f"Verify user : {user}")
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if user.otp == otp:
            # OTP is verified, mark user as verified
            login(request,user)
            messages.success(request, "Login Successfull")
            return redirect('home')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    
    return render(request, 'verify_login.html', {'email': email})






