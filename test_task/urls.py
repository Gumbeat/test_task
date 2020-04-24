"""test_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from test_task.app.views import (
    PostCreateView,
    PostListView,
    PostDetailView,
    PostDeleteView,
    UserActivityList,
    AppUserDetailView,
    LikeUnlikePost,
    AnalyticsListView
)

api_urlpatterns = [
    path('user/<int:pk>', AppUserDetailView.as_view(), name='user_detail'),
    path('user_activity/', UserActivityList.as_view(), name='user_activity'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_details'),
    path('posts/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('posts/create', PostCreateView.as_view(), name='post_create'),
    path('like_post/', LikeUnlikePost.as_view(), name='like_post'),
    path('analytics/', AnalyticsListView.as_view(), name='likes_analytics'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # /api/auth/users/ - login
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns))
]
