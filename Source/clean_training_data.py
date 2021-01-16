import nltk.corpus
import pandas as pd
from clean_data import clean_data

nltk.download("stopwords")
nltk.download("wordnet")


def open_file(path):
    with open(path, encoding="ISO-8859-1") as readfile:
        return pd.read_csv(
            readfile,
            engine="python",
            error_bad_lines=False,
            header=None,
        )


def get_data():
    path = "../Data/data.csv"
    df = open_file(path)
    return df[5], df[0]


def save_prepared_data(data, marks):
    data_to_save = data.apply(lambda tweet: " ".join(tweet))
    df = pd.DataFrame({"tweet": data_to_save, "mark": marks})
    df = df[df["tweet"].notna()]
    df.to_csv("../Data/prepared_data.csv", index=False)


x, y = get_data()
x = clean_data(x)
save_prepared_data(x, y)
