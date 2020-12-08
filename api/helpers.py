import glob
import os


def find_last_modified_recording():
    return max(
        glob.iglob(r"./assets/data/recordings/*.wav"), key=os.path.getmtime)


def find_last_modified_result():
    return max(
        glob.iglob(r"./assets/data/results/*.wav"), key=os.path.getmtime)


def get_taco_models():
    # to get the full file path
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

    # get folder names with model inside them
    # step 1: change \\ ==> /
    # step 2: get everything after checkpoints/ 
    # step 3: remove everything after underscore like ['_tts', '_raw']
    model_folders = [i.replace('\\', '/').split('checkpoints/')[1].split('_')[0] for i in glob.iglob(f"{dir_path}/models/checkpoints/*/")]

    # remove duplicates
    return list(dict.fromkeys(model_folders))
