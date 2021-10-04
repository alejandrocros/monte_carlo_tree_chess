import json

import numpy as np
import random


def save_array(filename: str, np_array: np.array) -> None:
    with open(filename, "wb") as savefile:
        np.save(savefile, np_array)


def save_table(filename: str, table_dict: dict) -> None:
    with open(filename, "w+") as savefile:
        json.dump(table_dict, savefile)


def load_previous_table(previous_training_path: str) -> dict:
    try:
        with open(previous_training_path, "r+") as fp:
            table = json.load(fp)
    except Exception as exc:
        print(f"Couldn't load the previous training due to {exc}")
        table = dict()
    return table


def reset_all_seeds(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
