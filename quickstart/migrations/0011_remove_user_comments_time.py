# Generated by Django 3.1.2 on 2021-03-11 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0010_auto_20210312_0050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_comments',
            name='time',
        ),
    ]