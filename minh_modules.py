import pandas as pd
import numpy as np

class Sampling_articles:
    NUMBER_OF_ARTICLES = 50

    def get_homepage_articles(data_dict, user_dict):
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
                #Divide articles into categories list it belonged to :) 
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
                f"Array empty bcs run out of articles with {magic} category, changing probabilities"
            if run_out_of_article:
                probs[user_category.index(magic)] = 0
                cal_prob()
            run_out_of_article = True
        return in_category_list + out_category_list
