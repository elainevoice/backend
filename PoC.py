import numpy as np
import pandas as pd
import pydub

from keras.layers import Dense, LSTM, LeakyReLU
from keras.models import Sequential, load_model
from scipy.io.wavfile import read, write
from tensorflow import keras
from datetime import datetime

class Predict:
    models = []

    def __init__(self, models):
        for i in models:
            self.models.append(keras.models.load_model(i))

    def predict(self, location, file_name = f'model_result_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav'):
        def _read_file(loc):
            rate, input_audio = read(loc)
            return rate, input_audio

        def _correct_amount_of_columns(df):
            if len(df.columns.values) < 2:
                df[1] = df[0]
            elif len(df.columns.values) > 2:
                raise Exception(f"there are to many columns. columns: {df.columns.values} ")
            return df
        
        def _create_train_dataset(df, look_back, train=True):
            dataX1, dataX2 , dataY1 , dataY2 = [],[],[],[]
            for i in range(len(df)-look_back-1):
                dataX1.append(df.iloc[i : i + look_back, 0].values)
                dataX2.append(df.iloc[i : i + look_back, 1].values)
                if train:
                    dataY1.append(df.iloc[i + look_back, 0])
                    dataY2.append(df.iloc[i + look_back, 1])
            if train:
                return np.array(dataX1), np.array(dataX2), np.array(dataY1), np.array(dataY2)
            else:
                return np.array(dataX1), np.array(dataX2)

        def _test_train_data(df, start, limit):
            # create data
            # X1, X2, y1, y2 = _create_train_dataset(pd.concat([df.iloc[0:start, :], df.iloc[0:start, :]], axis=0), look_back=3, train=True)
            test1, test2 = _create_train_dataset(pd.concat([df.iloc[start+1 : limit, :],df.iloc[start+1 : limit, :]], axis=0), look_back=3, train=False)

            # reshape
            # X1 = X1.reshape((-1, 1, 3))
            # X2 = X2.reshape((-1, 1, 3))
            test1 = test1.reshape((-1, 1, 3))
            test2 = test2.reshape((-1, 1, 3))
            return test1, test2 # X1, X2, y1, y2, test1, test2

        r, inp = _read_file(location)
        df = pd.DataFrame(inp)

        start_limit = int(len(df) / 4)
        max_limit = int(len(df))

        df = _correct_amount_of_columns(df)

        tests = _test_train_data(df, start_limit, max_limit)

        predictions = []
        for i in range(len(self.models)):
            predictions.append(self.models[i].predict(tests[i]))

        write(f'..\scripts\output\{file_name}', r, pd.concat([pd.DataFrame(predictions[0].astype('int16')), pd.DataFrame(predictions[1].astype('int16'))], axis=1).values)


model = [R'..\scripts\models\rnn1.h5', R'..\scripts\models\rnn2.h5']
p = Predict(model)
p.predict(R'..\scripts\assets\data\recordings\YAF_death_ps.wav')