from django.db.models import (
    Model,
    ForeignKey,
    DateField,
    CASCADE,
    OneToOneField,
    DateTimeField,
    TextField
)
from django.contrib.auth.models import User, update_last_login
from django.db.models.signals import post_save
from django.dispatch import receiver
from djoser.signals import user_activated, user_registered


class AppUser(Model):
    user = OneToOneField(User, related_name='app_user', on_delete=CASCADE)
    last_activity = DateTimeField(auto_now_add=True)

    @receiver(post_save, sender=User)
    def create_app_user(sender, instance, created, **kwargs):
        if created:
            AppUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_app_user(sender, instance, **kwargs):
        instance.app_user.save()

    @receiver(user_registered)
    @receiver(user_activated)
    def update_last_login(sender, user, request, *args, **kwargs):
        update_last_login(None, user)


    def __str__(self):
        return self.user.username


class Post(Model):
    user = ForeignKey(AppUser, related_name='app_user_post', on_delete=CASCADE)
    theme = TextField(max_length=256)

    def __str__(self):
        return self.theme


class Like(Model):
    created = DateField(auto_now_add=True)
    post = ForeignKey(Post, related_name='post_like', on_delete=CASCADE)
    user = ForeignKey(AppUser, related_name='app_user_like', on_delete=CASCADE)
