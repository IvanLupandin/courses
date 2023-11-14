from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_notification(user, posts):
    subject = 'Новые статьи в подписанных категориях'
    html_message = render_to_string('email_notification.html', {'posts': posts})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'NewsPortal14@gmail.com', [user.email], html_message=html_message)
