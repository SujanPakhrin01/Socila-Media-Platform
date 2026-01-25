from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    Role_choices = (
        ('admin','Admin'),
        ('user',"User"),
    )
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(unique=False)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    bio = models.CharField(max_length=100,blank=True)
    role = models.CharField(max_length=50, choices=Role_choices, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_liked_posts(self):
        return [l.post for l in self.likes.all() if l.like]

    def get_comments_on_my_posts(self):
        return Comment.objects.filter(post__user=self)


    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total_like(self):
        return self.likes.count()  
    
    def total_comments(self):
        return self.comments.count() 
    
    def __str__(self):
        return f"post by {self.user.username}"
    

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    post = models.ForeignKey(Post,on_delete= models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=True)  # default True means “liked”
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'post')
class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('like','Like'),
        ('comment','Comment'),
    )
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_notifications')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver_notifications')
    notification_type = models.CharField(max_length=10,choices=NOTIFICATION_TYPE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Analytics(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def total_posts(self):
        return self.user.posts.count()  # <- counts posts dynamically

    def __str__(self):
        return f"Analytics for {self.user.username}"



    

