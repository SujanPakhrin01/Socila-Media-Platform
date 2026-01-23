from django.shortcuts import render
from .models import *
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer, FollowSerializer, AnalyticsSerializer, NotificationSerializer,TagSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer

class Home(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def list(self, request):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    
class ProfileView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    search_fields = ['username']


    def list(self, request):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    
class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def list(self, request):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    
class NotifictionView(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def list(self, request):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
class FollowView(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]
    def list(self, request):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
class TagView(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def list(self, request):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
class LikeView(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def list(self, request):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
 


class AnalyticsView(ModelViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def list(self, request):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    
def NotificationChannel(request):
    return render(request,"index.html")



class SignupView(GenericAPIView):
    serializer_class = SignupSerializer 
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    