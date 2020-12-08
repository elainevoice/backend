import glob
import os


def find_last_modified_recording():
    return max(
        glob.iglob(r"./assets/data/recordings/*.wav"), key=os.path.getmtime)


def find_last_modified_result():
    return max(
        glob.iglob(r"./assets/data/results/*.wav"), key=os.path.getmtime)

def get_taco_models():
    # get real file path
    # got bs with relative path
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

    #get model folder names
    # step 1: removes static path
    # stap 2: removes thing like ['_tts', '_raw']
    model_folders = [i.replace('\\', '/').split('checkpoints/')[1].split('_')[0] for i in glob.iglob(f"{dir_path}/models/checkpoints/*/")]

    # remove duplicates
    return list(dict.fromkeys(model_folders))