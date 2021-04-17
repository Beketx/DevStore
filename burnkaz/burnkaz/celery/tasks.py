from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from burnkaz import settings

@shared_task
def send_email_task(email_to):
    send_mail('LASt of proofes',
              'LASt of proofes',
              settings.EMAIL_HOST_USER,
              [email_to, ])
    return None