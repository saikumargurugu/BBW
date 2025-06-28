from django.core.mail import send_mail
import os
import uuid
from django.conf import settings
from admin_api.models import Uploads

def send_otp_email(email, otp):
    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is {otp}. Please use this to verify your account.",
        from_email=os.getenv('EMAIL_HOST_USER'),
        recipient_list=[email],
        fail_silently=False,
    )


# //FILE UPLOAD HANDLER//
def handle_file_upload(file_obj, model_name='', url="draft/"):
    upload_dir = os.path.join(settings.MEDIA_ROOT, url)
    os.makedirs(upload_dir, exist_ok=True)
    file_ext = os.path.splitext(file_obj.name)[1]
    unique_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, unique_name)

    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    upload = Uploads.objects.create(
        unique_id=uuid.uuid4(),
        path=f"uploads/{unique_name}",
        model=model_name,
        file_size=file_obj.size,
        file_type=file_obj.content_type
    )
    return upload
