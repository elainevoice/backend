import numpy as np
import pandas as pd
import os
import random
from scipy.io.wavfile import read, write

path = R'assets/data/sounds_wav/words/'

number_of_sentences = 50
max_number_of_words = 9

#make dataframe
temp = []
for i in os.listdir(path):
    r, inp = read(path + i)
    if (all(j == 0 for j in inp)) == False:
        temp.append([i, inp])

df = pd.DataFrame(temp, columns=['name', 'data'])

for _ in range(number_of_sentences):
    # set values
    length_sentence = random.randint(2,max_number_of_words)
    blacklisted_words = []
    created_sentence = []
    res = []

    # select values
    for i in range(length_sentence):
        word = None
        while True:
            t = random.randint(1,len(df)-1)
            if t not in blacklisted_words:
                blacklisted_words.append(t)
                word = t
                break
        created_sentence.append(df.iloc[word]['name'])
        res.extend(df.iloc[word]['data'])

    # create name
    temp = ''
    f = True
    for i in created_sentence:
        i = i.replace('.wav', '')
        if f:
            temp += i
            f = False
        else:
            temp += '_' + i
    
    # write file
    created_sentence = temp + '.wav'
    write(f'./gen_sentence/{created_sentence}', 44100, np.array(res))
    print(created_sentence)
