from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ProfileView, Home, CommentView, NotifictionView, FollowView, TagView, LikeView, AnalyticsView
from App.views import SignupView

urlpatterns = [
    
    path('api/SignUp/', SignupView.as_view()),    
    path('api/Login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/Login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/Profile/', ProfileView.as_view({'get': 'list'}), name='profile'),
    path('api/Profile/<int:pk>/', ProfileView.as_view({'get': 'retrieve'}), name='profile-detail'),
    path('api/Home/', Home.as_view({'get': 'list','post':'create'}), name='home'),
    path('api/Comments/', CommentView.as_view({'get': 'list'}), name='comments'),
    path('api/Notifications/', NotifictionView.as_view({'get': 'list'}), name='notifications'),
    path('api/Notifications/pk', NotifictionView.as_view({'get': 'list'}), name='notifications'),
    path('api/Follows/', FollowView.as_view({'get': 'list'}), name='follows'),
    path('api/Tags/', TagView.as_view({'get': 'list'}), name='tags'),
    path('api/Tags/pk', TagView.as_view({'get': 'list'}), name='tags'),
    path('api/Likes/', LikeView.as_view({'get': 'list'}), name='likes'),
    path('api/Analytics/', AnalyticsView.as_view({'get': 'list'}), name='analytics')
]