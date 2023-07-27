from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        articles_rating = Post.objects.filter(author=self.user).aggregate(models.Sum('rating'))['rating__sum'] or 0
        comments_rating = Comment.objects.filter(post__author=self.user).aggregate(models.Sum('rating'))['rating__sum'] or 0
        articles_comments_rating = Comment.objects.filter(post__author=self.user).aggregate(models.Sum('rating'))['rating__sum'] or 0
        self.rating = articles_rating * 3 + comments_rating + articles_comments_rating
        self.save()

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    ARTICLE = 'article'
    NEWS = 'news'
    POST_TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        preview_length = 124
        if len(self.text) <= preview_length:
            return self.text
        else:
            return self.text[:preview_length] + "..."

    def __str__(self):
        dataf = 'Post from {}'.format(self.created_at.strftime('%d.%m.%Y %H:%M'))
        return f"{dataf},{self.author},{self.title}"

    def get_absolute_url(self):
        return reverse('Start')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post},from the category:  {self.category}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.created_at}, {self.user}"
