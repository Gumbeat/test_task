from django.contrib import admin
from .models import AppUser, Post

admin.site.register(AppUser)
admin.site.register(Post)
