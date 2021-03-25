from django.contrib.auth.models import User, Group
from django.db.models import fields
from . models import Article_Category, Article_Tags, Articles, Category, Tags, User_Comments, User_View, Users,User_Category
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','url', 'username', 'email', 'groups']

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ['userId', 'user_name', 'password', 'name', 'representation']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ['tagID','tag']

class Article_TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article_Tags
        fields = ['id','articleID','tagID']

class User_CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Comments
        fields=['commentID','userID','articleID', 'content', 'time']

class User_ViewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User_View
        fields=['userID', 'articleID', 'time']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields=['categoryID', 'category', 'level']

class Article_CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article_Category
        fields = ['id','articleID','categoryID']

class ArticlesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Articles
        fields = ['articleID', 'representation', 'link', 'category', 'displayContent', 'content','time', 'title', 'tags', 'sapo', 'thumbnail', 'click_counter','hot_score']

class User_CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User_Category
        fields = ['id','userID','categoryID','count']