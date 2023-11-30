from django.core.mail import send_mail
from django.contrib.auth.models import User


def send_newsletter(news_title, news_content):
    users = User.objects.all()
    recipients = [user.email for user in users]
    send_mail(
        news_title,
        news_content,
        'NewsPortal14@gmail.com',
        recipients,
        fail_silently=False,
    )