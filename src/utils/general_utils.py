import json

import numpy as np


def save_array(filename, np_array):
    with open(filename, "wb") as savefile:
        np.save(savefile, np_array)


def save_table(filename, table_dict):
    with open(filename, "w+") as savefile:
        json.dump(table_dict, savefile)


def load_previous_table(previous_training_path):
    try:
        with open(previous_training_path, "r+") as fp:
            table = json.load(fp)
    except Exception as exc:
        print(f"Couldn't load the previous training due to {exc}")
        table = dict()
    return table
