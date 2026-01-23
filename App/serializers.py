from . models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import User

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField(source = 'follower.count',read_only = True)
    following_count = serializers.IntegerField(source ='following.count',read_only = True )
    
    class Meta:
        model = User
        fields = [
            'id','username','email','profile_picture','bio','role','follower_count','following_count'
        ]        
        
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='User.username')
    likes_count = serializers.IntegerField(source='likes.count',read_only=True)
    commeng_count = serializers.IntegerField(source='comment.count',read_only=True)    
    class Meta:
        model = Post
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = '__all__'
        
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Like
        fields = '__all__'
        
        
class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.username')
    class Meta:
        model = Follow
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']

        if user == following:
            raise serializers.ValidationError("You can’t follow yourself")

        if Follow.objects.filter(
            follower=user, following=following
        ).exists():
            raise serializers.ValidationError("Already followed")

        return data

    def create(self, validated_data):
        validated_data['follower'] = self.context['request'].user
        return super().create(validated_data)
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = Notification
        fields = '__all__'
        
class AnalyticsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Analytics
        fields = '__all__'
        



class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    
    


