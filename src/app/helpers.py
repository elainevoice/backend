import glob


def find_last_modified_recording():
    return max(glob.iglob(R"./src/assets/data/recordings/*.wav"), key=os.path.getmtime)
