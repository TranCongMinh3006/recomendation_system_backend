# Generated by Django 3.1.2 on 2021-03-17 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0033_auto_20210317_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_comments',
            name='userID',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]