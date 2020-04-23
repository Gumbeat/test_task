from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    RelatedField,
    StringRelatedField
)
from django.contrib.auth.models import User
from .models import AppUser, Like, Post


class UserSerializer(ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class AppUserSerializer(ModelSerializer):
    last_login = SerializerMethodField()
    username = CharField(source='user.username', required=False)

    class Meta:
        model = AppUser
        fields = ['id', 'username', 'last_activity', 'last_login']
        related_fields = ['user']

    def get_last_login(self, obj):
        return User.objects.get(id=obj.user.id).last_login


class PostCreateSerializer(ModelSerializer):
      class Meta:
        model = Post
        fields = ['user', 'theme']


class LikeCreateSerializer(ModelSerializer):
      class Meta:
        model = Like
        fields = ['user', 'post']


class PostSerializer(ModelSerializer):
    creator_name = CharField(source='user.user.username')
    like_count = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'creator_name', 'theme', 'like_count']
        related_fields = ['user']

    def get_like_count(self, obj):
        return Like.objects.filter(post=obj).count()
