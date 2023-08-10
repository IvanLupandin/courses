from . import views
from django.urls import include, path
from .views import NewsList, NewsDetail, Search, NewsEdit, NewsDelete, ArticleCreate, ArticleEdit, ArticleDelete
from django.contrib.auth.views import LoginView, LogoutView
from .views import ProfileUpdateView, create_post, welcome_email
from .tasks import send_weekly_email_notifications

app_name = 'news'

urlpatterns = [
    path('', views.Start_Padge, name='Start'),  # URL-шаблон Стартовой страницы
    path('search/', Search.as_view(), name='search'),  # URL-шаблон Поисковой страницы
    path('news/', NewsList.as_view(), name='news_list'),  # URL-шаблон для списка новостей
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('article/', views.article_list, name='article_list'),  # URL-шаблон для списка статей
    path('<int:post_id>/', views.article_detail, name='article_detail'),
    path('news/create/', views.NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('accounts/', include('allauth.urls')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('create_post/', create_post, name='create_post'),
    path('send_weekly_notifications/', send_weekly_email_notifications, name='send_weekly_notifications'),
    path('welcome_email/', welcome_email, name='welcome_email'),
]
