import glob
import os
from api.config import models



def find_last_modified_recording():
    return max(glob.iglob(r"./assets/data/recordings/*.wav"), key=os.path.getmtime)


def find_last_modified_result():
    return max(glob.iglob(r"./assets/data/results/*.wav"), key=os.path.getmtime)


def get_taco_models():
    return models