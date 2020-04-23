from rest_framework.status import HTTP_201_CREATED, HTTP_202_ACCEPTED
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AppUser, Post, Like
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    PostCreateSerializer,
    AppUserSerializer,
    PostSerializer,
    LikeCreateSerializer
)


class AnalyticsListView(ListAPIView):
    queryset = Like.objects.all()

    def get_queryset(self, *args, **kwargs):
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        like_count = self.queryset.filter(created__range=[date_from, date_to]).count()
        return Response({'like_count': like_count})


class LikeUnlikePost(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Like.objects.all()
    serializer = LikeCreateSerializer

    def post(self, request, *args, **kwargs):
        post_id = request.data['post_id']
        user = AppUser.objects.get(user=request.user)
        if Like.objects.filter(user=user, post_id__exact=post_id).count() == 0:
            serializer = LikeCreateSerializer(data={'user': user.id, 'post': post_id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=HTTP_201_CREATED, data={'message': 'Post liked'})
        Like.objects.get(user=user, post_id__exact=post_id).delete()
        return Response(status=HTTP_202_ACCEPTED, data={'message': 'Post Unliked'})


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def post(self, request, *args, **kwargs):
        user = AppUser.objects.get(user=request.user)
        theme = request.data['theme']
        serializer = PostCreateSerializer(data={'user': user.id, 'theme': theme})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED, data={'message': 'Post created'})


class PostDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class UserActivityList(ListAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer


class AppUserListCreateView(ListCreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class AppUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
