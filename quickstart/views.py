from django.contrib.auth.models import User, Group
from . models import Article_Category, Article_Tags, Articles, Category, Tags, User_Comments, User_View, Users, User_Category
from rest_framework import viewsets
from rest_framework import permissions
from quickstart.serializers import Article_CategorySerializer, Article_TagsSerializer, ArticlesSerializer, CategorySerializer, UserSerializer, GroupSerializer, TagSerializer, User_CommentSerializer, User_ViewSerializer, UsersSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
import json
from django.http import JsonResponse
from rest_framework.response import Response
import datetime

#----------------------------------------------------------------

import pickle
import numpy as np 
import pandas as pd
import keras
from keras.layers import *
from keras.models import Model
from keras import backend as K
import tensorflow as tf

class Multiple_Score:
    def __init__(self, number_articles):
        user_rep = Input(shape=(768,), dtype='float32')
        candidates = [Input(shape=(768,), dtype='float32') for _ in range(number_articles)]
        logits = [keras.layers.dot([user_rep, candidate_vec], axes=-1) for candidate_vec in candidates]
        logits = keras.layers.Activation(keras.activations.sigmoid)(keras.layers.concatenate(logits))
        inputs_tt = candidates + [user_rep]
        self.Score = Model(candidates+[user_rep], logits)
number_articles = 200#len(all_articles_represent)
multiScore_model = Multiple_Score(number_articles)
print(multiScore_model)
#----------------------------------------------------------------

#--------------------------------------------------------------------

# time_now = int(datetime.datetime.now().timestamp())
# cache_days = 200
# time_72h_before = time_now - 60 * 60 * 24 * cache_days

# number_of_articles = 200
# # # -----------------------------------------------------------------
# # # chỗ này là các bài báo mới
# new_articles = Articles.objects.filter(time__gt=time_72h_before)[:number_of_articles]


# # # ----------------------------------------------------------------
# # # chỗ này là các bài báo hot
# hot_article_in72h = Articles.objects.filter(
#     time__gt=time_72h_before)
# hot_article_in72h_id = hot_article_in72h.values_list('articleID', flat=True)
# for i in list(hot_article_in72h_id):
#     tmp = Articles.objects.get(pk=i)
#     click_score = tmp.click_counter
#     ID = tmp.articleID
#     number_of_comments = User_Comments.objects.filter(
#         articleID=ID).count()

#     if click_score is not None:
#         hot_score = number_of_comments*9 + click_score
#     else:
#         hot_score = number_of_comments*10
#     tmp.hot_score = hot_score
#     tmp.save()

# hot_articles = Articles.objects.all().order_by('-hot_score',)[:number_of_articles]

# ------------------------------------------------
# chỗ này là các bài báo được load lên theo dạng aritcleId : representation sau khi runserver
all_articles_represent ={}
news = Articles.objects.all()[:200]
list_of_articleId = news.values_list('articleID', flat=True)
for x in list_of_articleId:
    all_articles_represent[x] = Articles.objects.get(pk=x).representation

test =all_articles_represent[x] 
print(type(test))
print(test)
def convert_article_rep():
    all_articles_represent_convert = dict()
    for articleID in all_articles_represent:
        represent = all_articles_represent[articleID]
        represent_reconvert = np.frombuffer(represent, dtype='float32').reshape(1,30,768)
        all_articles_represent_convert[articleID] = represent_reconvert
    return all_articles_represent_convert

# all_articles_represent_convert = convert_article_rep(all_articles_represent)
# print('conver oke:', len(all_articles_represent_convert))


# print(new_dic)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated]


class User_View_ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = User_View.objects.all()
    serializer_class = User_ViewSerializer
    permission_classes = [permissions.IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


class Article_Tags_ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Article_Tags.objects.all()
    serializer_class = Article_TagsSerializer
    permission_classes = [permissions.IsAuthenticated]


class User_Comment_ViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = User_Comments.objects.all()
    serializer_class = User_CommentSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticated]

# cai nay da ok vi no kha nhanh
    @action(detail=False)
    def get_top_level_category(self, request):
        new_article = Category.objects.filter(level=0)
        page = self.paginate_queryset(new_article)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(new_article, many=True)
        return Response(serializer.data)

# hàm lấy tất cả các bài theo category
#   đã ok nhưng thời gian chạy hơi lâu đặc biệt với các category với level cao như 0,
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        article_category = Article_Category.objects.filter(
            categoryID=instance.categoryID)[:20]
        lst = []
        for e in article_category:
            article1 = Articles.objects.get(articleID=e.articleID)
            lst.append(article1)
        lst1 = []
        for x in lst[:100]:  # trả về 100 bài báo theo category nhung chua phai la moi nhat
            dic = {
                'articleID': x.articleID,
            }
            lst1.append(dic)
        return JsonResponse(lst1, safe=False)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def get_personal_article(self, request):
        data = request.data
        userID = data['userID']
        repre_of_user = Users.objects.get(userId = userID).representation

        # load input article_rep for score
        multiple_inputs_newsEncoder = []
        for articleID in sample_candidate:
            article_represent = np.array(all_articles_represent_convert[articleID])
            input_newsEncoder = [userid_embedd, article_represent]
            candidate_rep = newsEncoder.news_encoder.predict(input_newsEncoder)
            multiple_inputs_newsEncoder.append(candidate_rep)
        print(len(multiple_inputs_newsEncoder))

        user_vector = userVector_dict[user]
        newsEncoder_sample = multiple_inputs_newsEncoder
        traingen = newsEncoder_sample + [user_vector]
        print(len(traingen))
        all_score = multiScore_model.Score.predict(traingen)

        end = time.time()
        print(f'time: {(end-start)/60}minutes')
        print(userID, repre_of_user)
        article_id = Articles.objects.all().order_by(
            '-time',)[:100].values_list('articleID', flat=True)
        dic = {}
        dic['articleID'] = list(article_id)
        return JsonResponse(dic)

#  đã ok , tim theo str trong form data
    @action(detail=False)
    def search(self, request):
        # data = request.data
        # print(data)
        # str1 = str(data['str'])
        article_id = Articles.objects.filter(title__contains = "hôm").order_by(
            '-time',)[:100].values_list('articleID', flat=True)
        dic = {}
        dic['articleID'] = list(article_id)
        return JsonResponse(dic)


# phần này đã ok , trả về artical detail  và tagid, commentid


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        obj = User_Category.objects.get(userID=1002722676)
        obj.count +=1
        obj.save()

        comment = User_Comments.objects.filter(
            articleID=instance.articleID).values_list('commentID', flat=True)
        tag = Article_Tags.objects.filter(
            articleID=instance.articleID).values_list('tagID', flat=True)
        dic = {
            'articleID': instance.articleID,
            'representation': instance.representation,
            'link': instance.link,
            'category': instance.category,
            'displayContent': instance.displayContent,
            'content': instance.content,
            'time': instance.time,
            'title': instance.title,
            'tags': instance.tags,
            'sapo': instance.sapo,
            'thumbnail': instance.thumbnail,
            'click_counter': instance.click_counter,
            'hot_score': instance.hot_score
        }
        dic['comments'] = list(comment)
        dic['tags'] = list(tag)
        return JsonResponse(dic)

# phần này đã ok
    @action(detail=False)
    def new_article(self, request):
        new_article = new_articles

        page = self.paginate_queryset(new_article)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(new_article, many=True)
        return Response(serializer.data)


# đã làm được nhưng thời gian quá lâu , cần cải thiện sau

    @action(detail=False)
    def hot_article(self, request):
        hot_article = hot_articles
        page = self.paginate_queryset(hot_article)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(hot_article, many=True)
        return Response(serializer.data)


class Article_CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Article_Category.objects.all()
    serializer_class = Article_CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class Article_CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Article_Category.objects.all()
    serializer_class = Article_CategorySerializer
    permission_classes = [permissions.IsAuthenticated]




# đã ok 
# import pickle

# file = open('resources/articles_rep_10k.pkl', 'rb')
# articles_represent = pickle.load(file)
# file.close()

# def update_representation_of_articles(dict):
#     for idx, x in enumerate(dict):
#             tmp = Articles.objects.get(pk = x)
#             tmp.representation = dict[x]
#             tmp.save()

# update_representation_of_articles(articles_represent)

# from django.http import HttpResponse
# import datetime

# def get_personal_article(request):
#     now = datetime.datetime.now()
#     html = "<html><body>It is now %s.</body></html>" % now
#     return HttpResponse(html)