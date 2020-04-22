from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AppUser, Post, Like
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import PostSerializer, AppUserSerializer, UserSerializer
from .. import settings


class PostListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.request.data.get('post_id'))  # toDo: поменять
        return serializer.save(post=post)


class PostDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)  # toDo: поменять, чтобы удалял только владелец
    queryset = Post.objects.all()
    serializer_class = PostSerializer


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

# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def authenticate_user(request):
#     try:
#         email = request.data['email']
#         password = request.data['password']
#
#         user = User.objects.get(email=email, password=password)
#         if user:
#             try:
#                 payload = jwt_payload_handler(user)
#                 token = jwt.encode(payload, settings.SECRET_KEY)
#                 user_details = {'name': f'{user.first_name} {user.last_name}', 'token': token}
#                 user_logged_in.send(sender=user.__class__,
#                                     request=request, user=user)
#                 return Response(user_details, status=status.HTTP_200_OK)
#
#             except Exception as e:
#                 raise e
#         else:
#             res = {
#                 'error': 'can not authenticate with the given credentials or the account has been deactivated'}
#             return Response(res, status=status.HTTP_403_FORBIDDEN)
#     except KeyError:
#         res = {'error': 'please provide a email and a password'}
#         return Response(res)
