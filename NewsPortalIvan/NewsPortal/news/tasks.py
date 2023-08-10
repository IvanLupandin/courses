import threading
from datetime import timedelta
from django.utils import timezone
from .models import Post, Subscription
from .utils import send_email_notification

def send_weekly_email_notifications():
    week_ago = timezone.now() - timedelta(days=7)
    new_posts = Post.objects.filter(created_at__gte=week_ago)
    subscriptions = Subscription.objects.all()

    for subscription in subscriptions:
        user = subscription.user
        subscribed_posts = [post for post in new_posts if post.category == subscription.category]
        if subscribed_posts:
            send_email_notification(user, subscribed_posts)

def start_send_weekly_email_notifications():
    thread = threading.Thread(target=send_weekly_email_notifications)
    thread.start()