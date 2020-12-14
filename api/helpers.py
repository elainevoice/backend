import glob
import os


def find_last_modified_recording():
    return max(glob.iglob(r"./assets/data/recordings/*.wav"), key=os.path.getmtime)


def find_last_modified_result():
    return max(glob.iglob(r"./assets/data/results/*.wav"), key=os.path.getmtime)

def _name_from_checkpoint_files(checkpoint_file):
    checkpoint_file = checkpoint_file.replace('\\', '/').split('checkpoints/')[1].split('_')[0]
    return checkpoint_file


def get_taco_models():
    # to get the full file path
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
    checkpoints_folder = glob.iglob(f"{dir_path}/models/checkpoints/*/")


    # get folder names with model inside them
    # step 1: change \\ ==> /
    # step 2: get everything after checkpoints/ 
    # step 3: remove everything after underscore like ['_tts', '_raw']
    model_folders = [_name_from_checkpoint_files(i) for i in checkpoints_folder]

    # remove duplicates
    return list(dict.fromkeys(model_folders))
