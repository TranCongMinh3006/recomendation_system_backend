# Generated by Django 3.1.2 on 2021-03-17 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0034_user_comments_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article_category',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='article_tags',
            name='articleID',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='article_tags',
            name='tagID',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='article_tags',
            unique_together=set(),
        ),
    ]