from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    Role_choices = (
        ('admin','Admin'),
        ('user',"User"),
    )
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    bio = models.CharField(max_length=100,blank=True)
    role = models.CharField(max_length=10,choices=Role_choices,default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"post by {self.user.username}"
    

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete= models.CASCADE, related_name='comments')
    text = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username}"

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete= models.CASCADE, related_name='likes')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','post')
  
    

class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"




class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)
    posts = models.ManyToManyField(Post,related_name='tags')
    
    def __str__(self):
        return self.name

class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('like','Like'),
        ('comment','Comment'),
        ('follow','Follow')
    )
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_notifications')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver_notifications')
    notification_type = models.CharField(max_length=10,choices=NOTIFICATION_TYPE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Analytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_posts = models.PositiveIntegerField(default=0)
    total_followers = models.PositiveIntegerField(default=0)
    total_following = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)


    

