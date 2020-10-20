import numpy as np
import pandas as pd

from scipy.io.wavfile import read, write
from tensorflow import keras
from datetime import datetime


class Predict:
    models = []

    def __init__(self, models):
        for i in models:
            self.models.append(keras.models.load_model(i))

    def _read_file(self, loc):
        rate, input_audio = read(loc)
        return rate, input_audio

    def _correct_amount_of_columns(self, df):
        if len(df.columns.values) < 2:
            df[1] = df[0]
        elif len(df.columns.values) > 2:
            raise Exception(f"there are too many columns. columns: {df.columns.values} ")
        return df
    
    def _create_test_dataset(self, df, look_back=3):
        data = [[] for i in range(len(df.columns.values))]
        for i in range(len(df)-look_back-1):
            for j in range(len(data)):
                data[j].append(df.iloc[i: i + look_back, j].values)

        res = []
        for i in data:
            res.append(np.array(i))        
        return res

    def _test_dataset(self, df, start, limit):
        tests = self._create_test_dataset(pd.concat([df.iloc[start+1: limit, :], df.iloc[start+1: limit, :]], axis=0))

        # reshape
        for i in range(len(tests)):
            tests[i] = tests[i].reshape((-1, 1, 3))
        return tests

    def predict(self, location, file_name=f'model_result_{str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))}.wav'):
        r, inp = self._read_file(location)
        df = pd.DataFrame(inp)

        start_limit = int(len(df) / 4)
        max_limit = int(len(df))

        df = self._correct_amount_of_columns(df)
        tests = self._test_dataset(df, start_limit, max_limit)

        predictions = []
        for i in range(len(self.models)):
            predictions.append(self.models[i].predict(tests[i]))

        write(f'..\scripts\output\{file_name}', r, pd.concat([pd.DataFrame(predictions[i].astype('int16')) for i in range(len(predictions))], axis=1).values)


p = Predict([R'..\scripts\models\output\rnn1.h5', R'..\scripts\models\output\rnn2.h5'])
p.predict(R'..\scripts\assets\data\recordings\YAF_death_ps.wav')
