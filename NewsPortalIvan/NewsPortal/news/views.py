from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .utils import send_email_notification
from .filters import PostFilter
from .forms import NewsForm, ArticleForm, PostForm
from .models import Post, Category, Profile, Subscription
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

"""
get_object_or_404 - используется для получения объекта из базы данных по заданным условиям. 
Если объект не найден, то функция вызывает исключение `Http404`, и возвращает страницу с ошибкой 404.
"""


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            # Отправка уведомления пользователям, подписанным на категорию статьи
            subscriptions = Subscription.objects.filter(category=post.category)
            users = [subscription.user for subscription in subscriptions]
            send_email_notification(users, [post])

            return redirect('home')
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'create_post.html', context)


@login_required
def welcome_email(request):
    user = request.user
    subject = 'Добро пожаловать в наше приложение!'
    html_message = render_to_string('welcome_email.html')
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'noreply@example.com', [user.email], html_message=html_message)
    return render(request, 'welcome_email_sent.html')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['name', 'email']
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'myapp.add_post'
    model = Post
    fields = ['title', 'content']
    template_name = 'post_create.html'
    success_url = reverse_lazy('home')


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'myapp.change_post'
    model = Post
    fields = ['title', 'content']
    template_name = 'post_update.html'
    success_url = reverse_lazy('home')


# ====== Стартовая страница ============================================================================================
def Start_Padge(request):
    news = Post.objects.filter(type='NW').order_by('-creationDate')[:4]
    return render(request, 'flatpages/Start.html', {'news': news})


# ====== Новости =======================================================================================================
class NewsList(ListView):
    paginate_by = 10
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset().filter(type='NW')
        return queryset.order_by('-creationDate')


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'


class NewsCreate(CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'news_create.html'
    success_url = '/'

    def form_valid(self, post):
        post = post.save(commit=False)
        post.categoryType = 'NW'
        post.Author = self.request.user.author
        post.save()
        return super().form_valid(post)


class NewsEdit(UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'news_edit.html'
    success_url = '/'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = '/'


# ====== Статьи ========================================================================================================
def article_list(request):
    article = Post.objects.filter(type='AR').order_by('-creationDate')  # Фильтруем только статьи
    # и сортируем по убыванию даты
    paginator = Paginator(article, 2)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'news/article_list.html', {'articles': articles})


def article_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'news/article_detail.html', {'post': post})


class ArticleCreate(CreateView):
    model = Post
    form_class = ArticleForm
    template_name = 'article_create.html'
    success_url = '/'

    def form_valid(self, post):
        post = post.save(commit=False)
        post.categoryType = 'AR'
        post.Author = self.request.user.author
        post.save()
        return super().form_valid(post)


class ArticleEdit(UpdateView):
    model = Post
    form_class = ArticleForm
    template_name = 'article_edit.html'
    success_url = '/'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = '/'


# ====== Поиск =========================================================================================================
class Search(ListView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filterset_class = PostFilter
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['categories'] = Category.objects.all()  # Получение всех категорий
        return context
