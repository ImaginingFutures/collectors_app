from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings

def send_password_reset_email(request, user):
    domain = request.get_host()  # Retrieves the domain used in the request
    protocol = 'https' if request.is_secure() else 'http'
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    password_reset_url = f"{protocol}://{domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

    subject = "Password Reset Requested"
    message = f"Please click the following link to reset your password: {password_reset_url}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    send_mail(subject, message, from_email, to_email, fail_silently=False)
