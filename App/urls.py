from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ProfileView, Home, CommentView, NotifictionView, FollowView, TagView, LikeView, AnalyticsView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/profile/', ProfileView.as_view({'get': 'list'}), name='profile'),
    path('api/home/', Home.as_view({'get': 'list'}), name='home'),
    path('api/comments/', CommentView.as_view({'get': 'list'}), name='comments'),
    path('api/notifications/', NotifictionView.as_view({'get': 'list'}), name='notifications'),
    path('api/follows/', FollowView.as_view({'get': 'list'}), name='follows'),
    path('api/tags/', TagView.as_view({'get': 'list'}), name='tags'),
    path('api/likes/', LikeView.as_view({'get': 'list'}), name='likes'),
    path('api/analytics/', AnalyticsView.as_view({'get': 'list'}), name='analytics')
]