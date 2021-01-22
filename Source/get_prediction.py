import calendar
import os
import pickle  # noqa
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def open_file(path):
    with open(path, encoding="cp1252") as readfile:
        df = pd.read_csv(readfile)
    df = df[df["tweet"].notna()]
    return df["tweet"], df["date"]


def get_dictionary():
    with open("../Data/dict.txt", "rb") as file:
        return pickle.load(file)  # noqa


def preapare_tweets(x):
    max_tweet = max(x, key=lambda tweet: len(tweet.split()))
    max_tweet_len = len(max_tweet.split())
    x = x.apply(lambda tweet: tweet.split())
    words = get_dictionary()
    for tweet in x:
        for j, word in enumerate(tweet):
            if word in words.keys():
                tweet[j] = words[word]
            else:
                tweet[j] = 0
    return pad_sequences(x, maxlen=max_tweet_len)


def get_predictions(x):
    model = load_model("../SimpleRNN_batch_size_128.h5", compile=False)
    model.compile(
        loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]
    )  # noqa
    return model.predict_classes(x)


def pie_plot(predictions, name):
    results = Counter(np.hstack(predictions))
    colors = ("#de425b", "#9fc08f")
    diag = pd.Series({"negative": results[0], "positive": results[1]})
    plot = diag.plot.pie(colors=colors, autopct="%1.1f%%")
    plot.set_ylabel("")
    plot.set_title(f"@{name}'s annual mood statistic per 2020")
    plt.savefig(f"../Users/{name}/{name}_pie_plot.png")


def group_barplot(predictions, date, name):
    date = date.apply(lambda date: date.split("-"))
    month = date.apply(lambda date: int(date[1]))
    data = pd.DataFrame()
    data["month"] = month
    data["predictions"] = predictions
    indexes = [calendar.month_abbr[x] for x in range(1, 13)]
    negative = (
        data[data.predictions == 0].groupby("month")["predictions"].size().to_frame()
    )
    positive = (
        data[data.predictions == 1].groupby("month")["predictions"].size().to_frame()
    )
    negative = negative.reindex(list(range(1, 13)))
    df = negative.merge(
        positive, how="left", on="month", suffixes=("_negative", "_positive")
    ).fillna(0)
    df.index = indexes
    colors = ["#de425b", "#478c30"]
    plot = df[["predictions_negative", "predictions_positive"]].plot.bar(color=colors)
    plot.set_title(f"@{name}'s annual mood statistic per month")
    plt.savefig(f"../Users/{name}/{name}_bars_plot.png")


def create_plots(name):
    path = f"../Users/{name}/cleaned_{name}.csv"
    tweets, date = open_file(path)
    tweets = preapare_tweets(tweets)
    predictions = get_predictions(tweets)
    pie_plot(predictions, name)
    group_barplot(predictions, date, name)
