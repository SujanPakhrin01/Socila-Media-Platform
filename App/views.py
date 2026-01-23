from django.shortcuts import render
from .models import *
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer, FollowSerializer, AnalyticsSerializer, NotificationSerializer,TagSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group

class Home(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username','id']

    def list(self, request):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    
class ProfileView(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['id','username']
    
    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        elif self.action == 'retrieve':
            return [AllowAny()]
        return super().get_permissions()
    

    def list(self, request):       
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    
    def retrieve(self, request,pk=None):
        user = self.get_object()  # gets the user with the given pk
        serializer = self.get_serializer(user)
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
 


class AnalyticsView(GenericViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAdminUser]

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
            group = Group.objects.get(name='user')  # now this works
            user.groups.add(group)
            user.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Automatically set as normal user
        user.is_user = True  # or any field you have for normal users
        user.save()
        return user
    
    