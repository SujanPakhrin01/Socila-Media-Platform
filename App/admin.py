from django.contrib import admin
from .models import User, Post, Comment, Like, Follow, Tag, Notification, Analytics

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    
class LikeInline(admin.TabularInline):
    model = Like
    extra = 0

admin.site.register(User)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'image')
    inlines = [CommentInline, LikeInline]
    
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Analytics)
# admin.site.register(Notification)



