from django.contrib import admin

from .models import Author, Category, Post, Comment, PostCategory

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostCategory)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # ... другие настройки администратора ...

    @admin.permissions('myapp.add_post', 'myapp.change_post')
    def has_view_permission(self, request, obj=None):
        # Проверяем, принадлежит ли пользователь к группе "authors"
        if request.user.groups.filter(name='authors').exists():
            return True
        return super().has_view_permission(request, obj)

    @admin.permissions('myapp.add_post', 'myapp.change_post')
    def has_add_permission(self, request):
        # Проверяем, принадлежит ли пользователь к группе "authors"
        if request.user.groups.filter(name='authors').exists():
            return True
        return super().has_add_permission(request)

    @admin.permissions('myapp.change_post')
    def has_change_permission(self, request, obj=None):
        # Проверяем, принадлежит ли пользователь к группе "authors"
        if request.user.groups.filter(name='authors').exists():
            return True
        return super().has_change_permission(request, obj)