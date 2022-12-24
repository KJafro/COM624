import os
import numpy as np
import math
from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
class Prediction:
    def __init__(self,groups):
        self.groups = groups
    def create_base_model