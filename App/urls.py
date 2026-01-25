from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import ProfileView, Home, CommentView, NotifictionView, LikeView, AnalyticsView
from App.views import SignupView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('api/SignUp/', SignupView.as_view()),    
    path('api/Login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/Login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('api/Profile/', ProfileView.as_view({'get': 'list','post':'create'}), name='profile'),
    path('api/Profile/<int:pk>/', ProfileView.as_view({'get': 'retrieve','put': 'update', 'patch': 'partial_update','delete': 'destroy',}), name='profile-detail'),
    
    path('api/Home/', Home.as_view({'get': 'list','post':'create'}), name='home-list'),
    path('api/Home/<int:pk>/', Home.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}), name='home-detail'),
    
    path('api/Comments/', CommentView.as_view({'post':'create'}), name='comments'),
    # path('api/Notifications/', NotifictionView.as_view({'get': 'list'}), name='notifications'),
    # path('api/Notifications/pk', NotifictionView.as_view({'get': 'list'}), name='notifications'),
    path('api/Like/', LikeView.as_view({'post':'create'}), name='likes'),
    path('api/Analytics/', AnalyticsView.as_view({'get': 'list'}), name='analytics'),
    path('api/Analytics/<int:pk>/', AnalyticsView.as_view({'get': 'retrieve'}), name='analytics')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)