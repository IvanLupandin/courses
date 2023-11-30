from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('create/', views.create_advertisement, name='create_advertisement'),
    path('<int:pk>/edit/', views.edit_advertisement, name='edit_advertisement'),
    path('responses/private/', views.private_responses, name='private_responses'),
    path('<int:pk>/send_response/', views.send_response, name='send_response'),
    path('account/login/', auth_views.LoginView.as_view(), name='login'),
    # Другие URL-шаблоны
]