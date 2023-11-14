from django.apps import AppConfig
import redis


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'


    def ready(self):
        import NewsPortal.news.signals

red = redis.Redis(
    host='redis-10332.c273.us-east-1-2.ec2.cloud.redislabs.com',
    port=10332,
    password='3AhbR1HWfwmnKftX15RqkoPH7SzcLPmI'
)
