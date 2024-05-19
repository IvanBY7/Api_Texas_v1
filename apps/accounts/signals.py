# # apps/accounts/signals.py

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from .tasks import send_verification_email
# from django.contrib.sites.shortcuts import get_current_site
# User = get_user_model()

# @receiver(post_save, sender=User)
# def send_verification_email_signal(sender, instance, **kwargs):
#      if kwargs.get('created', False):
#         current_site = get_current_site(request=None)
#         domain = current_site.domain
#         send_verification_email.delay(instance.id, domain)
