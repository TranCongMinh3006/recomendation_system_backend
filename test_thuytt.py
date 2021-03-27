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

userEmbedd = keras.models.load_model('./resources/user_embedd_model')
print(userEmbedd)
file = open('./resources/userid_dict.pkl', 'rb')
userid_dict = pickle.load(file)
file.close()


userID = 1063372939
# userID = 4977
# if userID not in userid_dict:
#     userid_dict[]
userid = np.array([userID], dtype='uint64')
print(userid.shape)
print(userid)
userEmbedd.predict(userid)