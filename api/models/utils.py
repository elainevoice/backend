import pathlib
import os
from pydub import AudioSegment
import pandas as pd


class Utils:
    @staticmethod
    def mp3_to_wav(path):
        try:
            for path in pathlib.Path(path).iterdir():
                sound = AudioSegment.from_mp3(path)
                dest = f"{path.parent}/{path.stem}.wav"
                print(dest)
                sound.export(dest, format="wav")
        except Exception as e:
            print(e)

    @staticmethod
    def rename_wav():
        words = pd.read_csv('../assets/data/words_dict_nl.csv')
        sentences = pd.read_csv('../assets/data/sentences_dict_nl.csv')

        directory = "../assets/data/sounds_wav/sentences"
        for filename in os.listdir(directory):
            turks = filename[:-4].lower()
            match = sentences.loc[sentences['turks'] == f"sounds/sentences/{turks}.mp3"]
            nederlands = match['nederlands'].item().replace(' ', '_')
            old_file = os.path.join(directory, filename)
            new_filename = old_file.replace(turks, nederlands)
            try:
                os.rename(old_file, new_filename)
            except:
                pass


def format_wavs():
    Utils.mp3_to_wav("../../assets/data/sounds_mp3/sentences")
    Utils.mp3_to_wav("../../assets/data/sounds_mp3/words")
