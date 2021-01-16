import pickle  # noqa
from collections import Counter, OrderedDict

import numpy as np
import pandas as pd


def open_file(path):
    with open(path, encoding="cp1252") as readfile:
        df = pd.read_csv(readfile)
    df = df[df["tweet"].notna()]
    df = df.sample(frac=1)  # mix data
    return df["tweet"], df["mark"]


def create_dict_for_network():
    path = "../Data/prepared_data.csv"
    x, y = open_file(path)
    x = x.apply(lambda tweet: tweet.split())
    new_x = np.hstack(x)
    words_dict = OrderedDict(Counter(new_x).most_common())
    return dict(zip(words_dict.keys(), range(1, 65001)))


def save_dict():
    with open("../Data/dict.txt", "wb") as file:
        pickle.dump(create_dict_for_network(), file)


save_dict()
