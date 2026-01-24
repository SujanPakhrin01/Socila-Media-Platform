from . models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model 


User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField(source = 'follower.count',read_only = True)
    following_count = serializers.IntegerField(source ='following.count',read_only = True )
    
    class Meta:
        model = User
        fields = [
            'id','username','email','profile_picture','bio','role','follower_count','following_count'
        ]
        
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Comment
        fields = ['id', 'user', 'created_at','text']
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = '__all__'
        
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.IntegerField(source='total_like', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    liked_by = LikeSerializer(source='likes',many=True,read_only=True
)

    class Meta:
        model = Post
        fields = ['id','user','content','image','likes_count','liked_by','comments','created_at','updated_at',]
        read_only_fields = ['id','user','likes_count','liked_by','comments','created_at', 'updated_at', ]
        
        
        
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
        fields = ['username','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    
    


