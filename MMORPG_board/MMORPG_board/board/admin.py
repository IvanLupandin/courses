from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # определяем, какие поля отображать в списке новостей
    search_fields = ('title', 'content')  # добавляем возможность поиска по заголовку и содержимому новостей

admin.site.register(News, NewsAdmin)