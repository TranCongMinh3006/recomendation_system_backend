from django.contrib.auth.models import User, Group
from . models import Article_Category, Article_Tags, Articles, Category, Tags, User_Comments, User_View, Users, User_Category
from rest_framework import viewsets
from rest_framework import permissions
from quickstart.serializers import Article_CategorySerializer, Article_TagsSerializer, ArticlesSerializer, CategorySerializer, UserSerializer, GroupSerializer, TagSerializer, User_CommentSerializer, User_ViewSerializer, UsersSerializer,User_CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
import json
from django.http import JsonResponse
from rest_framework.response import Response
import datetime

#----------------------------------------------------------------

# thuytt load all class
import operator
import random
import time
import pickle
import numpy as np 
import pandas as pd
import keras
from keras.layers import *
from keras.models import Model
from keras import backend as K
import tensorflow as tf

# load models and file pkl
file = open('./resources/phobert_embed_mat.pkl', 'rb')
embedding_mat = pickle.load(file)
file.close()

# load userid_dict
file = open('./resources/userid_dict.pkl', 'rb')
userid_dict = pickle.load(file)
file.close()

userEmbedd = keras.models.load_model('./resources/user_embedd_model')
print(userEmbedd)



#--------------------------------------------------------------------
# define cache_days
time_now = int(datetime.datetime.now().timestamp())
cache_days = 4
time_72h_before = time_now - 60 * 60 * 24 * cache_days

# number articles save cache
number_of_articles = 10
print(f'number of articles in cache: {number_of_articles}')

# # # -----------------------------------------------------------------
# # # chỗ này là các bài báo mới
print('begin load time 72h')
new_articles = Articles.objects.filter(time__gt=time_72h_before)[:number_of_articles]
print(len(new_articles))
print(len(new_articles))
# new_articles = new_articles[:number_of_articles]
print(type(new_articles))

# number_of_articles = min(number_of_articles, len(new_articles))


class Multiple_Score:
    def __init__(self, number_articles):
        print('Initialize Multiple_Score_Model\n')
        user_rep = Input(shape=(768,), dtype='float32')
        candidates = [Input(shape=(768,), dtype='float32') for _ in range(number_articles)]
        logits = [keras.layers.dot([user_rep, candidate_vec], axes=-1) for candidate_vec in candidates]
        logits = keras.layers.Activation(keras.activations.sigmoid)(keras.layers.concatenate(logits))
        inputs_tt = candidates + [user_rep]
        self.Score = Model(candidates+[user_rep], logits)

multiScore_model = Multiple_Score(number_of_articles)

class NewsEncoder:
    def __init__(self, embedding_mat):
        print('Initialize NewsEncoder_Model\n')
        self.__embedding_dim = embedding_mat.shape[1]
        
        userid_dense_input = Input(shape=(200,), dtype='float32')
        news_cnn_input = Input(shape=(30,768,), dtype='float32')
        attention_a = Dot((2, 1))([news_cnn_input, Dense(self.__embedding_dim, activation='tanh')(userid_dense_input)])
        attention_weight = Activation('softmax')(attention_a)
        news_rep = keras.layers.Dot((1, 1))([news_cnn_input, attention_weight])
        self.news_encoder = Model([userid_dense_input, news_cnn_input], news_rep)

newsEncoder = NewsEncoder(embedding_mat)
#----------------------------------------------------------------


# # # ----------------------------------------------------------------
# # chỗ này là các bài báo hot
print('Load hot articles......................')
hot_article_in72h = Articles.objects.filter(
    time__gt=time_72h_before)
print('finish hot filers')
hot_article_in72h_id = hot_article_in72h.values_list('articleID', flat=True)
print(len(hot_article_in72h_id))
for i in list(hot_article_in72h_id):
    tmp = Articles.objects.get(pk=i)
    click_score = tmp.click_counter
    ID = tmp.articleID
    number_of_comments = User_Comments.objects.filter(
        articleID=ID).count()

    if click_score is not None:
        hot_score = number_of_comments*9 + click_score
    else:
        hot_score = number_of_comments*10
    tmp.hot_score = hot_score
    tmp.save()

hot_articles = Articles.objects.filter(time__gt=time_72h_before).order_by('-hot_score',)[:number_of_articles]
print('Done load hot news', len(hot_articles))
# ------------------------------------------------
# chỗ này là các bài báo được load lên theo dạng aritcleId : representation sau khi runserver
print('Load represent articles.............')
all_articles_represent ={}
# news = new_articles[:100]
# print(news)
# print('news:..............', news.count())
list_of_articleId = new_articles.values_list('articleID', flat=True)
print('listofArticleId:..............')
for x in list_of_articleId:
    print('load article represent', x)
    all_articles_represent[x] = Articles.objects.get(pk=x).representation

# reconvert articles represent CNNoutput
def convert_article_rep(all_articles_represent):
    all_articles_represent_convert = dict()
    for articleID in all_articles_represent:
        represent = all_articles_represent[articleID]
        represent = json.loads(represent)
        represent_reconvert = np.array(represent, dtype='float32').reshape(1,30,768) # reshape list to np.array
        all_articles_represent_convert[articleID] = represent_reconvert
    return all_articles_represent_convert
print('run function convert_article_rep')
all_articles_represent_convert = convert_article_rep(all_articles_represent)
print('convert oke:', len(all_articles_represent_convert))
print('Done load articles rep')

# print(new_dic)

# ----------------------------------------------------------
# đây là chỗ load 1 dic article va category tuong ung
article_category_dict = {}

for x in new_articles.values_list('articleID', flat=True):
    category_id = Article_Category.objects.filter(
                articleID=x).values_list('categoryID', flat=True)
    for cateID in category_id:
        tmp_categoryID = Category.objects.get(pk=cateID)
        if tmp_categoryID.level == 0:
            article_category_dict[x] = tmp_categoryID.categoryID # sửa lỗi cho Minh, phải dạng articleID - categoryID

print('article-cate:',len(article_category_dict), article_category_dict)
# ---------------------------------------------------------------

user_category_count_dict= dict()


# dic['articleID'] = list(article_id)




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

class User_CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = User_Category.objects.all()
    serializer_class = User_CategorySerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def post_user_category(self, request, *args, **kwargs):
        data = request.data
        userID = data['userID']
        categoryIDs = data['categoryIDs'].split(',')
        for x in categoryIDs:
            tmp = User_Category.objects.get(categoryID = int(x) , userID = userID)
            tmp.count = 1
            tmp.save()
        dic ={}
        dic['status_post'] = "ok"
        return JsonResponse(dic)


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    # permission_classes = [permissions.IsAuthenticated]

#get_userID_and_status
    @action(detail=False, methods=['post'])
    def get_userID_and_status(self, request, *args, **kwargs):
        data = request.data
        username = data['username']
        userID = User.objects.get(username=username).id

        check_user_exist = Users.objects.filter(
            userId=userID).count()

        status = 1
        if check_user_exist == 0:   
            init_user = Users.objects.get(pk = -1)
            new_user = Users(userId=userID, representation = init_user.representation)
            new_user.save()
            categorys_list = Category.objects.all().values_list('categoryID', flat=True)
            uer_categorys_list = User_Category.objects.all().values_list('id', flat=True)
            number_user_category_records = len(uer_categorys_list)
            if number_user_category_records ==0:
                maxID = 0
            else:
                maxID = max(uer_categorys_list)
            for x in list(categorys_list):
                obj = User_Category(id = maxID + 1,userID=userID,categoryID=x,count =0)
                maxID +=1
                obj.save()  
            status = 0
        dic = {}
        dic['status'] = status
        # usersID = User.objects.get(username = username)
        dic['userID'] = userID
        dic['username'] = username
        return JsonResponse(dic)


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
    @action(detail=False, methods=['post'])
    def get_comment_by_articleID(self, request):
        data = request.data
        articleID = data['articleID']
        comments_by_articleID = User_Comments.objects.filter(articleID=articleID)
        page = self.paginate_queryset(comments_by_articleID)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(comments_by_articleID, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def post_comment(self, request):
        data = request.data
        articleID = data['articleID']
        userID = data['userID']
        content = data['content']
        time = datetime.datetime.now().timestamp()
        arr_comments = list(User_Comments.objects.all().values_list('commentID', flat=True))
        if(len(arr_comments) == 0):
            id = 1
        else:
            id  = max(arr_comments) + 1
        tmp = User_Comments(commentID = id, articleID=articleID, userID=userID, content=content, time = time  )
        tmp.save()
        dic ={}
        dic['status_post'] = "ok"
        return JsonResponse(dic)


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

# hàm lấy tất cả các bài theo category , ham nay da ok
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        article_id = Article_Category.objects.filter(
            categoryID=instance.categoryID).values_list('articleID', flat=True)
        dic = {}
        dic['articleID'] = list(article_id)
        return JsonResponse(dic)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=False,methods=['post'])
    def get_personal_article(self, request):
        start = time.time()
        data = request.data
        print(data)
        userID = data['id']
        print('userID from frontend:', userID)
        user_rep = Users.objects.get(userId = userID).representation
        user_rep = json.loads(user_rep) # do loi
        user_rep_convert = np.array(user_rep, dtype='float32').reshape(1,768)
        print(user_rep_convert.shape)

        # --------------------------------------------------------------------
        # begin NPA model
        # day la cho load 1 dic category va count tuong ung voi user
        user_category_tmp = User_Category.objects.filter(userID = userID).values_list('id', flat=True)
        user_category_tmp = list(user_category_tmp)
        print('user_category is here')
        for x in user_category_tmp:
            tmp = User_Category.objects.get(pk=x)
            print('for user_category_tmp', x)
            user_category_count_dict[tmp.categoryID]=tmp.count
        
        # -------------------------------------------------------------------
        # load candiate (ở cache), prepare var data
        sample_candidate = list(all_articles_represent_convert)
        
        userid = userID # userid user for train model
        if userid not in userid_dict:
            userid = random.randint(0, (len(userid_dict)-1) )
        userid = np.array([userid], dtype='uint64') 
        print(userid.shape)
        userid_embedd = userEmbedd.predict(userid)
        print(userid_embedd)

        # load input article_rep for score
        multiple_inputs_newsEncoder = []
        for articleID in sample_candidate:
            print('load input rep:', articleID)
            article_represent = np.array(all_articles_represent_convert[articleID])
            print('article convert:', article_represent.shape)
            input_newsEncoder = [userid_embedd, article_represent]
            candidate_rep = newsEncoder.news_encoder.predict(input_newsEncoder)
            multiple_inputs_newsEncoder.append(candidate_rep)
        print(len(multiple_inputs_newsEncoder))

        user_vector = user_rep_convert
        newsEncoder_sample = multiple_inputs_newsEncoder
        traingen = newsEncoder_sample + [user_vector]
        print(len(traingen))
        all_score = multiScore_model.Score.predict(traingen)

        end = time.time()
        print(f'time: {(end-start)/60}s')
        
        # return score sort articleID
        print('all_score',all_score.shape)
        score_dict = dict()
        for idx, articleID in enumerate(sample_candidate):
            score_dict[articleID] = all_score[0][idx]
        score_sort_dict = dict( sorted(score_dict.items(), key=operator.itemgetter(1),reverse=True))
        # print(score_sort_dict)

        # fake data count for category
        # user_category_count_dict={
        #     "1": 2,
        #     "2": 3,
        #     "3": 5
        # }

        #--------------------------------------------------------------------
        # đây là hàm để sampling data
        print('Day la sampling data------------------------------')
        start = time.time()
        NUMBER_OF_ARTICLES = 50
        def get_homepage_articles(data_dict, user_dict):
            #Get articles categories id
            user =  [[int(key), user_dict[key]] for key in user_dict]
            user_category = [category[0] for category in user] 
            # Check probability
            user.insert(0, [0, 0]) 
            user_category_df = pd.DataFrame(user, columns=['categoryID', 'count'])
            user_category_df['prob'] = 0.0
            def cal_prob():
                sum = 0
                for category_score in user_category_df['count']:
                    sum += category_score
                sum_prob = 0
                for index, row in user_category_df.iterrows():
                    prob = row['count']/sum
                    sum_prob += prob
                    user_category_df.at[index, 'prob'] = sum_prob
            cal_prob()   
            article_list =  [[key, data_dict[key]] for key in data_dict]
            articles_df = pd.DataFrame(article_list, columns = ['articleID', 'category'])
            in_category_df = pd.DataFrame(columns = ['articleID'])

            #Divide articles into two lists    
            in_category_list = []
            out_category_list = []
            for index, row in articles_df.iterrows():
                if row['category'] in user_category:
                    in_category_df = in_category_df.append(articles_df.loc[index])
                else:
                    out_category_list.append(articles_df.loc[index]['articleID'])
            run_out_of_article = True
            for j in range(NUMBER_OF_ARTICLES):
                magic = random.random()
                for i in range(len(user_category_df.index) - 1):
                    if user_category_df.iloc[i]['prob'] <= magic and magic <= user_category_df.iloc[i+1]['prob']:
                        id = int(user_category_df.iloc[i+1]['categoryID'])
                        for index, row in in_category_df.iterrows():
                            if id == row['category']:
                                in_category_list.append(row['articleID'])
                                in_category_df = in_category_df.drop(index = index)
                                run_out_of_article = False
                                break
                        if run_out_of_article:
                            user_category_df.at[i, 'count'] = 0
                            cal_prob()
                        run_out_of_article = True
                if len(in_category_df.index) == 0:
                    return in_category_list + out_category_list
            return in_category_list + out_category_list
        
        articles_list_return = (get_homepage_articles(article_category_dict, user_category_count_dict))
        articles_list_return = [int(x) for x in articles_list_return]
        print(articles_list_return[0:10])
        print(type(articles_list_return[0]))
        end = time.time()
        print(f'Time run sampling MinhMoc: {(end-start)}s', )
        
        # CongMinh code return format for frontend
        dic = {}
        dic['articleID'] = list(articles_list_return)
        return JsonResponse(dic)

#search  đã ok , tim theo str trong form data
    @action(detail=False,methods=['post'])
    def search(self, request):
        data = request.data
        str = data['str']
        article_id = Articles.objects.filter(title__contains = str).order_by(
            '-time',)[:100].values_list('articleID', flat=True)
        dic = {}
        dic['articleID'] = list(article_id)
        # print(dic)
        return JsonResponse(dic)


# phần này đã ok , trả về artical detail  và tagid, commentid


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(request.data)
        # phan nay can them tang cho bang user_category them 1 va them biet time vao User_view
        # obj = User_Category.objects.get(userID=1002722676)
        # obj.count +=1
        # obj.save()

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
        dic['tags'] = list(tag)
        return JsonResponse(dic)

#new_article phần này đã ok
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
#hot_articles
    @action(detail=False)
    def hot_article(self, request):
        hot_article = hot_articles
        print(hot_article)
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




'''
Import user_representation into User table in mysql
# only use one time
'''
# import pickle
# import json
# file = open('resources/userVector_dict_json.pkl', 'rb')
# users_represent = pickle.load(file)
# file.close()

# def update_representation_of_users(user_dict):
#     print('update representation of users:\n-----------------------')
#     for idx, uid in enumerate(user_dict):
#         # if(idx<2):
#             user_obj = Users.objects.create(pk = uid)
#             print(user_obj)
#             tmp.representation = user_dict[uid]
#             tmp.save()

# update_representation_of_users(users_represent)

