# apps/accounts/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from .models import User
from django.conf import settings

@shared_task
def send_verification_email(user_id, domain):
    user = User.objects.get(pk=user_id)
    print("Enviando correo")
    subject = 'Por favor, activa tu cuenta.'
    html_message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER  # Reemplaza con tu dirección de correo electrónico
    to_email = user.email
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
