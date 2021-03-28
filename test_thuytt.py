import operator
import time
import pickle
import numpy as np 
import pandas as pd
import keras
from keras.layers import *
from keras.models import Model
from keras import backend as K
import tensorflow as tf
import os

# os.environ["CUDA_VISIBLE_DEVICES"]="0"
userEmbedd = keras.models.load_model('./resources/user_embedd_model1')
print(userEmbedd)
# print(userEmbedd.summary())
file = open('./resources/userid_dict.pkl', 'rb')
userid_dict = pickle.load(file)
file.close()


userID = 1003507211
# userID = 4977
# if userID not in userid_dict:
#     userid_dict[]
userid = userid_dict[1003507211]
userid = np.array([userid], dtype='uint64')
print(userid.shape)
# print(userid)
predictor = userEmbedd.predict(userid)
print(predictor.shape, predictor)