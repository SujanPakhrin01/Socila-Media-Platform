from django.shortcuts import render
from .models import *
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer, FollowSerializer, AnalyticsSerializer, NotificationSerializer
from rest_framework.views import APIView
# Create your views here.



