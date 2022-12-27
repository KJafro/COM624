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

        # Training Model

    def create_base_model(self,df,ticker):
        data = df.filter(['Close'])
        dataset = data.values
        scaler = MinMaxScaler(feature_range=(0, 1))
        training_data_len = math.ceil(len(dataset) * 0.8)
        train_data = scaler.fit_transform(dataset)
        train_data = train_data[0:training_data_len, :]
        x_train = []
        y_train = []
        for i in range(60, len(train_data)):
            x_train.append(train_data[i - 60:i, 0])
            y_train.append(train_data[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, batch_size=1, epochs=1)

        prev_60_days = data[-60:].values
        prev_60_days_scaled = scaler.transform(prev_60_days)
        today_data = data[-61:-1].values
        today_data_scaled = scaler.transform(today_data)
        today_data = data.iloc[-1].values

        X_test = []
        X_test.append(prev_60_days_scaled)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        X_test_2 = []
        X_test_2.append(today_data_scaled)
        X_test_2 = np.array(X_test_2)
        X_test_2 = np.reshape(X_test_2, (X_test_2.shape[0], X_test_2.shape[1], 1))

        nextday_pred_price = model.predict(X_test)
        nextday_pred_price = scaler.inverse_transform(nextday_pred_price)
        today_pred_price = model.predict(X_test_2)
        today_pred_price = scaler.inverse_transform(today_pred_price)

        nextday_pred_price = round(float(nextday_pred_price[0][0]), 2)
        today_pred_price = round(float(today_pred_price[0][0]), 2)
        today_data = round(today_data[0], 2)
        return nextday_pred_price, today_pred_price, today_data

        # Loading Model JSON

    def load_pred_model(self, df, ticker):
        load_json = os.path.join(os.getcwd(), "models", f"{ticker}.json")
        load_json2 = os.path.join(os.getcwd(), "models", f"{ticker}.h5")
        with open(load_json, "r") as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json)
        model.load_weights(load_json2)
        model.compile(optimizer='adam', loss='mean_squared_error')
        data = df.filter(['Close'])
        dataset = data.values
        scaler = MinMaxScaler(feature_range=(0, 1))
        train_data = scaler.fit_transform(dataset)
        prev_60_days = data[-60:].values
        prev_60_days_scaled = scaler.transform(prev_60_days)
        today_data = data[-61:-1].values
        today_data_scaled = scaler.transform(today_data)
        today_data = data.iloc[-1].values

        X_test = []
        X_test.append(prev_60_days_scaled)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        X_test_2 = []
        X_test_2.append(today_data_scaled)
        X_test_2 = np.array(X_test_2)
        X_test_2 = np.reshape(X_test_2, (X_test_2.shape[0], X_test_2.shape[1], 1))
        nextday_pred_price = model.predict(X_test)
        nextday_pred_price = scaler.inverse_transform(nextday_pred_price)
        today_pred_price = model.predict(X_test_2)
        today_pred_price = scaler.inverse_transform(today_pred_price)
        nextday_pred_price = round(float(nextday_pred_price[0][0]), 2)
        today_pred_price = round(float(today_pred_price[0][0]), 2)
        today_data = round(today_data[0], 2)
        return nextday_pred_price, today_pred_price, today_data

        # Predicting new model/loading model

    def predict(self, df, ticker):
        if self.groups.group(ticker):
            nextday_pred_price, today_pred_price, today_data = self.load_pred_model(df, ticker)
        else:
            nextday_pred_price, today_pred_price, today_data = self.create_base_model(df, ticker)
        return nextday_pred_price, today_pred_price, today_data