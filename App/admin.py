from django.contrib import admin
from .models import User, Post, Comment, Like, Notification, Analytics

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    
class LikeInline(admin.TabularInline):
    model = Like
    extra = 0

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('id', 'username', 'email')
    list_filter = ('role', 'is_staff', 'is_active')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'image')
    inlines = [CommentInline, LikeInline]
    
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Analytics)
# admin.site.register(Notification)



