import pathlib
import os
from pydub import AudioSegment
import pandas as pd
import csv
import shutil

class Utils:

    @staticmethod
    def mp3_to_wav(path):
        try:
            for path in pathlib.Path(path).iterdir():
                sound = AudioSegment.from_mp3(path)
                dest = f"{path.parent}/{path.stem}.wav"
                sound.export(dest, format="wav")
        except Exception as e:
            print(e)

    @staticmethod
    def rename_wav():
        words = pd.read_csv("../assets/data/words_dict_nl.csv")
        sentences = pd.read_csv("../assets/data/sentences_dict_nl.csv")

        directory = "../assets/data/sounds_wav/sentences"
        for filename in os.listdir(directory):
            turks = filename[:-4].lower()
            match = sentences.loc[sentences["turks"] == f"sounds/sentences/{turks}.mp3"]
            nederlands = match["nederlands"].item().replace(" ", "_")
            old_file = os.path.join(directory, filename)
            new_filename = old_file.replace(turks, nederlands)
            try:
                os.rename(old_file, new_filename)
            except:
                pass

    @staticmethod
    def rename_dysarthia(basepath: str):
        k = 1
        chars = "\n,![].?'#/"
        dest = basepath + 'All/'
        data = {
            0: {
                'name': 'F01',
                'noSessions': 1
            },
            1: {
                'name': 'F03',
                'noSessions': 3
            },
            2: {
                'name': 'F04',
                'noSessions': 2
            }
        }

        # Loop over the different people/sessions.
        for person in data:
            path = basepath + data[person]['name']

            for sessionId in range(data[person]['noSessions']):
                prompts = path + f'/Session{sessionId+1}/prompts'
                wavs = path + f'/Session{sessionId+1}/audio'

                for file in os.listdir(prompts):
                    with open(prompts + '/' + file) as f:
                        prompt = f.readlines()[0]

                        # Replace forbidden chars.
                        for c in chars:
                            prompt = prompt.replace(c, "")

                        # Replace spaces in prompt to underscore and rename the file from ID to prompt.
                        prompt = prompt.replace(" ", "_").lower()
                        old_file = os.path.join(wavs + '/', file)
                        shutil.copy(old_file[:-3] + 'wav', dest)

                        while True:
                            try:
                                # Try renaming the file, if it fails, up the count with 1 since duplicate promps exists.
                                prefix = f"{data[person]['name']}_{sessionId+1}_{k}#"
                                new_filename = f"{dest}{prefix + prompt}.wav"
                                os.rename(f"{dest}{file[:-3]}wav", new_filename)
                                k = 1
                                break
                            except Exception as e:
                                if k == 10:
                                    break
                                else:
                                    print(e)
                                    k += 1

    @staticmethod
    def generate_csv(basepath):
        data_sentences = []

        for file in os.listdir(basepath):
            filename = file[:-4]
            print(filename)
            prompt = filename.split('#')[1].lower()
            prompt_normaal = prompt.replace('_', ' ')
            row = [filename, prompt_normaal, prompt_normaal]
            data_sentences.append(row)

        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerows(data_sentences)


def format_wavs():
    Utils.mp3_to_wav("../../assets/data/sounds_mp3/sentences")
    Utils.mp3_to_wav("../../assets/data/sounds_mp3/words")
