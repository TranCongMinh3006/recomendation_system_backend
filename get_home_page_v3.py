import pandas as pd
import random
import time
import numpy as np

NUMBER_OF_ARTICLES = 500
user_dict = {
    "1": 5,
    "2": 5,
    "3": 15
}
data_dict = {
    12456: 1
}
for i in range(1000):
    data_dict[random.randint(0, 10000)] =  random.randint(0, 3)
time1 = 0.0 
time2 = 0.0
def get_homepage_articles(data_dict, user_dict):
    global time1
    t = time.time()
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
            if user_category_df.iloc[i]['prob'] <= magic <= user_category_df.iloc[i+1]['prob']:
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
            time1 = time.time() - t
            return in_category_list +out_category_list
    time1 = time.time() - t
    return in_category_list + out_category_list
def get_homepage_articles_v2(data_dict, user_dict):
    global time2
    t = time.time()
    #Get articles categories id
    user_category = [int(key) for key in user_dict]
    user_category_count = [user_dict[key] for key in user_dict]

    category_article_list = {}
    for category in user_category:
        category_article_list[category] = []
    # Check probability
    probs = [0]*len(user_category)
    def cal_prob():
        total = sum(user_category_count)
        for i in range(len(user_category)):
            probs[i] = user_category_count[i]/total
    cal_prob()   
    article_list =  [[key, data_dict[key]] for key in data_dict]
    articles_df = pd.DataFrame(article_list, columns = ['articleID', 'category'])
    #Divide articles into two lists    
    in_category_list = []
    out_category_list = []
    for index, row in articles_df.iterrows():
        if row['category'] in user_category:
            category_article_list[row['category']].append(row['articleID'])
        else:
            out_category_list.append(articles_df.loc[index]['articleID'])
    run_out_of_article = True
    for j in range(NUMBER_OF_ARTICLES):
        magic = np.random.choice(user_category,p= probs)
        try:
            in_category_list.append(category_article_list[magic].pop(0))
            run_out_of_article = False
        except:    
            "Do nothing"
        if run_out_of_article:
            probs[user_category.index(magic)] = 0
            cal_prob()
        run_out_of_article = True
    time2 = time.time() - t
    return in_category_list + out_category_list

old = get_homepage_articles(data_dict, user_dict)
new = get_homepage_articles_v2(data_dict, user_dict)
print (f"f1 run in {time1} seconds, \nf2 run in {time2} seconds, \nwhich makes it faster {time1/time2:.2f} times")
