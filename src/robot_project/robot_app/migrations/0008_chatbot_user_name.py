# Generated by Django 3.0.7 on 2020-07-22 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('robot_app', '0007_remove_chatbot_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbot',
            name='user_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
