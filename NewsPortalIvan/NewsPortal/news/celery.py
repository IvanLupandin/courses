import os
from celery import Celery

# Установите переменную окружения с именем вашего проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# Создайте экземпляр класса Celery
app = Celery('your_project')

# Загрузите настройки из файла settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из модулей Django
app.autodiscover_tasks()