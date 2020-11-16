from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import pydub
import os
from keras.layers import Dense, LSTM, LeakyReLU
from keras.models import Sequential, load_model
from scipy.io.wavfile import read, write
from tensorflow import keras
from datetime import datetime

class LSTM1:
    def __init__(self):
        self.date = str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))

    music1 = None
    music2 = None
    music1_limit = None
    music2_limit = None
    music1_beginlimit = None
    music2_beginlimit = None
    rate = None
    df = None
    X_train1= None

    def get_files(self, directory):
        files = []
        for filename in os.listdir(directory):
            rate, music = read(f"{directory}/{filename}")
            filename = filename[:-4]
            filename = filename.replace('_', ' ')
            files.append([filename, rate, music])
        return files

    def load_data(self):
        data = self.get_files("../assets/data/sounds_wav/words")
        data += self.get_files("../assets/data/sounds_wav/sentences")

        df = pd.DataFrame(data, columns=['name', 'rate', 'data'])
        df = shuffle(df)
        df.reset_index(inplace=True, drop=True)
        self.df = df
        print(self.df)

        """
        sound = pydub.AudioSegment.from_mp3(r"../assets/data/recordings/eminem.mp3")
        sound.export(r"../assets/data/recordings/eminem.wav", format="wav")

        # loading the wav files
        self.rate, music1 = read(r'../assets/data/recordings/recording_08-10-2020_19-01-20.wav')
        music1_limit = int(len(music1) / 4)
        self.music1_beginlimit = int(len(music1) / 8)
        # taking only some part of the songs and converting to a dataframe
        music1 = pd.DataFrame(music1[0:music1_limit])

        rate, music2 = read(r'../assets/data/recordings/eminem.wav')
        music2_limit = int(len(music2) / 4)
        self.music2_beginlimit = int(len(music2) / 8)
        music2 = pd.DataFrame(music2[0:music2_limit])

        self.music1 = music1
        self.music2 = music2
        """


        #return music1, music2, music1_limit, music2_limit, music1_beginlimit, music2_beginlimit

    def correct_amount_of_columns(self, df):
        if len(df.columns.values) < 2:
            df[1] = df[0]
        elif len(df.columns.values) > 2:
            raise Exception(f"There are too many columns. Nr of columns: {df.columns.values} ")
        return df

    def create_train_dataset(self, df, look_back, train=True):
        dataX1, dataX2, dataY1, dataY2 = [], [], [], []
        for i in range(len(df) - look_back - 1):
            # Array van getallen
            dataX1.append(df.iloc[i: i + look_back, 0].values)
            dataX2.append(df.iloc[i: i + look_back, 1].values)
            if train:
                # Getal
                dataY1.append(df.iloc[i + look_back, 0])
                dataY2.append(df.iloc[i + look_back, 1])
        if train:
            return np.array(dataX1), np.array(dataX2), np.array(dataY1), np.array(dataY2)
        else:
            return np.array(dataX1), np.array(dataX2)

    def train(self):
        self.load_data()

        train, test = train_test_split(self.df, test_size=0.2)

        X_train = train['data']
        y_train = train['name']
        X_test = test['data']
        y_test = test['name']

        #X1, X2, y1, y2 = self.create_train_dataset(self.concat_df(), look_back=3, train=True)

        i = 0
        X_train1 = []
        for row in X_train.iteritems():
            try:
                X_train1.append(row[1].reshape(1, int(len(row[1])/3), 3))
            except Exception as e:
                print(e)
                pass
        print(X_train1)
        self.X_train = X_train1

        nn_model = self.create_model()
        print(nn_model.summary())
        nn_model.fit(np.array(X_train1), y_train, epochs=1, batch_size=100)
        nn_model.model.save(f'./generated_models/rnn-{self.date}.h5')

    def test(self):
        #test1, test2 = self.create_train_dataset(self.concat_df(), look_back=3, train=False)

        train, test = train_test_split(self.df, test_size=0.2)

        X_train = train['data']
        y_train = train['name']
        X_test = test['data']
        y_test = test['name']

        rnn1 = keras.models.load_model(f'./generated_models/rnn-{self.date}.h5')
        pred_rnn1 = rnn1.predict(X_test)

        write('pred_rnn.wav', self.rate, pd.concat([pd.DataFrame(pred_rnn1.astype('int16'))], axis=1).values)

        # saving the original music in wav format
        write('original.wav', self.rate, self.concat_df().values)

    def predict(self):
        rnn = keras.models.load_model(f'./generated_models/rnn20-10-2020_11-49-20.h5')

        rate, input_audio = read(r'../assets/data/recordings/YAF_death_ps.wav')

        # Convert wav array to dataframe
        input_audioframe = pd.DataFrame(input_audio)

        input_audioframe_startlimit = int(len(input_audioframe) / 4)
        input_audioframe_maxlimit = int(len(input_audioframe))

        # Add second column (channel) if it doesn't exist
        input_audioframe = self.correct_amount_of_columns(input_audioframe)

        test1, test2 = self.create_train_dataset(
            pd.concat([input_audioframe.iloc[input_audioframe_startlimit + 1: input_audioframe_maxlimit, :],
                       input_audioframe.iloc[input_audioframe_startlimit + 1: input_audioframe_maxlimit, :]], axis=0),
            look_back=3, train=False)

        test1 = test1.reshape((-1, 1, 3))
        pred_rnn1 = rnn.predict(test1)

        write(f'./generated_audio/pred_rnn-{self.date}.wav', rate, pd.concat([pd.DataFrame(pred_rnn1.astype('int16'))], axis=1).values)

        # saving the original music in wav format
        write(f'./generated_audio/original-rnn-{self.date}.wav', rate,
              pd.concat([input_audioframe.iloc[input_audioframe_startlimit + 1: input_audioframe_maxlimit, :],
                         input_audioframe.iloc[input_audioframe_startlimit + 1: input_audioframe_maxlimit, :]],
                        axis=0).values)

    def concat_df(self):
        return pd.concat([self.music1.iloc[self.music1_beginlimit + 1: self.music1_limit, :],
                          self.music2.iloc[self.music2_beginlimit + 1: self.music2_limit, :]],
                         axis=0)

    def create_model(self):
        nn_model = Sequential()
        nn_model.add(LSTM(units=100, activation='relu', input_shape=(None, 3)))
        nn_model.add(Dense(units=50, activation='relu'))
        nn_model.add(Dense(units=25, activation='relu'))
        nn_model.add(Dense(units=12, activation='relu'))
        nn_model.add(Dense(units=1, activation='relu'))
        nn_model.compile(optimizer='adam', loss='mean_squared_error')
        return nn_model


lstm = LSTM1()
lstm.train()