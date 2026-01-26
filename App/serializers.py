from . models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model 

User = get_user_model()


class UserSerializer(serializers.ModelSerializer): 
    User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField(source = 'follower.count',read_only = True)
    following_count = serializers.IntegerField(source ='following.count',read_only = True )
    
    class Meta:
        model = User
        fields = [
            'id','username','email','profile_picture','bio','role']
        
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    content = serializers.CharField(source='text')  # Map 'text' to 'content' for frontend
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        # Map 'text' back when creating
        text = validated_data.pop('text', None)
        return Comment.objects.create(text=text, **validated_data)
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'like', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
        
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    liked_by_users = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'likes_count', 'is_liked', 
                  'liked_by_users', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'likes_count', 'is_liked', 
                           'liked_by_users', 'comments', 'created_at', 'updated_at']
    
    def get_likes_count(self, obj):
        return obj.likes.filter(like=True).count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user, like=True).exists()
        return False
    
    def get_liked_by_users(self, obj):
        likes = obj.likes.filter(like=True).select_related('user')
        return [{'username': like.user.username, 'id': like.user.id} for like in likes]

        
        
class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = Notification
        fields = '__all__'
        
class AnalyticsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    total_posts = serializers.SerializerMethodField()  # dynamic field

    class Meta:
        model = Analytics
        fields = ['user', 'total_posts']  # list fields explicitly

    def get_total_posts(self, obj):
        return obj.user.posts.count()  # counts posts dynamically



class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    
    


