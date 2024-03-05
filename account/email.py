from django.core.mail import send_mail
import random
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.html import format_html

User=get_user_model()

def send_otp_via_email(email):
    subject='Account Verification Email'
    otp=random.randint(100000,999999)
    message = f'Use this OTP <strong>{otp}</strong> to Verify your email'
    email_from = settings.EMAIL_HOST

    send_mail(subject, "", email_from, [email],html_message=message)

    user=User.objects.get(email=email)
    user.otp=otp
    user.save()

def send_otp(otp,email):
    subject='Account Login Email'
    message = f'Use this OTP <strong>{otp}</strong> to Login to your Account'
    email_from = settings.EMAIL_HOST

    send_mail(subject, "", email_from, [email],html_message=message)


    


