# Generated by Django 2.2.4 on 2020-04-22 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200422_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='app_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
