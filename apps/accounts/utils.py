# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
# from django.urls import reverse
# from django.conf import settings

# def send_verification_email(request, user):
#     current_site = get_current_site(request)
#     mail_subject = 'Activate your account.'
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)
#     domain = current_site.domain
#     link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
#     activate_url = f"http://{domain}{link}"
    
#     message = render_to_string('account/activation_email.html', {
#         'user': user,
#         'domain': domain,
#         'uid': uid,
#         'token': token,
#         'activate_url': activate_url,
#     })
    
#     send_mail(
#         mail_subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [user.email],
#     )