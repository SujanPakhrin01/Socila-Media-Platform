from django.shortcuts import render
from .models import *
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer, AnalyticsSerializer, NotificationSerializer,SignupSerializer
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from rest_framework import mixins, filters
from rest_framework.permissions import ( IsAuthenticated, IsAdminUser, AllowAny)
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
User = get_user_model()
from .permissions import IsOwnerOrAdmin
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser  #for image to appera in front end 



class Home(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username','id']
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        # instantiate permission classes
        if self.action == 'list':
            return [AllowAny()]  # anyone can view list
        elif self.action in ['retrieve', 'create']:
            return [IsAuthenticated()]  # must be logged in
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]  # plus maybe your custom owner permission
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """
        Preview object before update or delete
        """
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)  
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
 
    
class ProfileView(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,GenericViewSet):   
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
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return super().get_permissions()
    
class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the text from 'content' field (frontend sends 'content')
        text = request.data.get('content')
        post_id = request.data.get('post')
        
        if not text or not post_id:
            return Response(
                {"error": "Post and content are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create comment with 'text' field
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            text=text
        )
        
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED
        )
    
    
class NotifictionView(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def list(self, request):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

class LikeView(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get('post')
        
        if not post_id:
            return Response({"error": "Post required"}, status=400)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

        # Check if user already liked this post
        existing_like = Like.objects.filter(user=user, post=post).first()
        
        if existing_like:
            if existing_like.like:
                # Unlike: set like to False or delete
                existing_like.delete()
                liked = False
            else:
                # Re-like
                existing_like.like = True
                existing_like.save()
                liked = True
        else:
            # Create new like
            Like.objects.create(user=user, post=post, like=True)
            liked = True

        return Response({
            "post": post.id,
            "likes_count": post.likes.filter(like=True).count(),
            "liked": liked
        }, status=200)

class AnalyticsView(ModelViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer
    authentication_classes = [JWTAuthentication] 
    
    permission_classes = [IsAdminUser]

    def list(self, request):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    
# def NotificationChannel(request):
#     return render(request,"index.html")




class SignupView(GenericAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        
        # Create or get the 'user' group
        group, created = Group.objects.get_or_create(name='user')
        user.groups.add(group)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
