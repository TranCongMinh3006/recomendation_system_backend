# Generated by Django 3.1.2 on 2021-03-15 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quickstart', '0024_remove_user_comments_articleid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_comments',
            name='articleID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quickstart.articles'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_comments',
            name='userID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
