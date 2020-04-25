from datetime import datetime, timedelta, date

from rest_framework.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_200_OK
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AppUser, Post, Like
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    PostCreateSerializer,
    AppUserSerializer,
    PostSerializer,
    LikeCreateSerializer
)


def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


class AnalyticsListView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeCreateSerializer

    def get(self, request, *args, **kwargs):
        df_str = 'date_from'
        dt_str = 'date_to'
        if df_str in request.GET and dt_str in request.GET:
            date_from = datetime.strptime(request.GET.get(df_str), "%Y-%m-%d")
            date_to = datetime.strptime(request.GET.get(dt_str), "%Y-%m-%d")
            analytics_data = []
            for single_date in date_range(date_from, date_to):
                like_count = self.queryset.filter(created=single_date.date()).count()
                analytics_data.append({'date': single_date.date(), 'like_count': like_count})
            return Response(status=HTTP_200_OK, data=analytics_data)
        like_count = self.queryset.all().count()
        return Response(status=HTTP_200_OK, data={'like_count': like_count})


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
        new_post = serializer.save()
        return Response(status=HTTP_201_CREATED, data={'message': 'Post created', 'post_id': new_post.id})


class PostDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class UserActivityList(ListAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer


class AppUserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
