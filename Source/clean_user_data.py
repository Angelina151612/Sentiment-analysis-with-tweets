import nltk.corpus
import pandas as pd

from Source.clean_data import clean_data

nltk.download("stopwords")
nltk.download("wordnet")


def open_file(path):
    with open(path, encoding="ISO-8859-1") as readfile:
        return pd.read_csv(readfile, sep="\t", comment="#")


def get_data(path):
    df = open_file(path)
    return df["tweet"], df["date"]


def save_prepared_data(data, date, path):
    data_to_save = data.apply(lambda tweet: " ".join(tweet))
    df = pd.DataFrame({"tweet": data_to_save, "date": date})
    df = df[df["tweet"].notna()]
    df.to_csv(path, index=False)


def cleaning(name):
    path = f"../Users/{name}/{name}.csv"
    x, date = get_data(path)
    x = x.apply(str)
    x = clean_data(x)

    path = f"../Users/{name}/cleaned_{name}.csv"
    save_prepared_data(x, date, path)
