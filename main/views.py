
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from account.email import send_otp_via_email,send_otp
from django.urls import reverse
import random
from django.contrib.auth.decorators import login_required,permission_required
from .models import Course,CourseContent

User=get_user_model()


def home_page(request):
    if request.user.is_authenticated:
        email = request.user.email
        user = User.objects.get(email=email)
        full_name = user.get_full_name()
        return render(request, 'index.html', {'name': full_name})
    return render(request, 'index.html', {'name': 'User'})

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
        group, created = Group.objects.get_or_create(name="Teacher")
        user.groups.add(group)
    elif registration_type=='student':
        user.is_student=True
        group, created = Group.objects.get_or_create(name="Student")
        user.groups.add(group)
   
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

def handle_exception(request, exception):
    print('method called')
    # Get the exception class name
    exception_name = exception.__class__.__name__

    print(exception_name)

    status_code = 403 if exception_name=='PermissionDenied' else 500
    # Render the exception template with the exception details
    return render(request, 'exception.html', {
        'exception_name': exception_name,
        'status_code': status_code
    })

@login_required(login_url='login')
@permission_required(['main.add_course','main.view_course','main.change_course','main.delete_course'],raise_exception=True)
def teacher_dashboard(request):
    courses = Course.objects.filter(teacher=request.user)
    name=request.user.name()
    return render(request,'teacher/dashboard.html',{'courses':courses,'name':name})

@login_required(login_url='login')
@permission_required(['main.add_course'],raise_exception=True)
def add_course(request):
    user=request.user

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course_price = request.POST.get('course_price')
        cover_image = request.FILES.get('cover_image')

        content_title = request.POST.get('content_title')
        content = request.FILES.get('content')
        
        # Create a new Course object with the uploaded file
        course = Course.objects.create(
            title=title,
            description=description,
            course_price=course_price,
            cover_image=cover_image,
            teacher=user
        )

        CourseContent.objects.create(
            course=course,
            content_title=content_title,
            content=content
        )
        messages.success(request,"Course Added!")
        return redirect('teacher dashboard')
    
    return render(request,'teacher/addcourse.html')

@login_required(login_url='login')
@permission_required(['main.change_course'],raise_exception=True)
def edit_course(request,id):
    course=Course.objects.get(id=id)
    content=CourseContent.objects.get(course=course)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course_price = request.POST.get('course_price')
        cover_image = request.FILES.get('cover_image')

        content_title = request.POST.get('content_title')
        contentFile = request.FILES.get('content')
        
        # Create a new Course object with the uploaded file
        course.title = title
        course.description = description
        course.course_price = course_price

        if cover_image:
            course.cover_image = cover_image

        course.save()

        content.course=course
        content.content_title=content_title

        if contentFile:
            content.content=contentFile

        content.save()
        messages.success(request,"Course Edited Successfully!")
        return redirect('teacher dashboard')
    return render(request,'teacher/editcourse.html',{'course':course,'content':content})

@login_required(login_url='login')
@permission_required(['main.delete_course'],raise_exception=True)
def delete_course(request,id):
    course=Course.objects.get(id=id)

    if request.method=="POST":
        confirm_delete=request.POST.get('confirm_delete')

        if confirm_delete=='yes':
            CourseContent.objects.filter(course=course).delete()
            course.delete()
            messages.success(request,"Course Deleted!")
            return redirect('teacher dashboard')
        elif confirm_delete=='no':
            return redirect('teacher dashboard')


    return render(request,'teacher/delete.html',{"course":course})

