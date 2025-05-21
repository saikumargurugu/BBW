from django.core.mail import send_mail
import os

def send_otp_email(email, otp):
    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is {otp}. Please use this to verify your account.",
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[email],
        fail_silently=False,
    )