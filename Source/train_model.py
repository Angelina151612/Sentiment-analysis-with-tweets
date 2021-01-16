import pickle  # noqa

import numpy as np
import pandas as pd
import seaborn as sns
from tensorflow.keras.layers import Dense, Embedding, SimpleRNN
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences


def open_file(path):
    with open(path, encoding="cp1252") as readfile:
        df = pd.read_csv(readfile)
    df = df[df["tweet"].notna()]
    df = df.sample(frac=1)  # mix data
    return df["tweet"], df["mark"]


def get_max_len(tweets):
    maximum = 0
    for tweet in tweets:
        words = len(tweet)
        if words > maximum:
            maximum = words
    return maximum


def get_dictionary():
    with open("../Data/dict.txt", "rb") as file:
        return pickle.load(file)  # noqa


def preapare_tweets(x):
    max_tweet_len = get_max_len(x)
    x = x.apply(lambda tweet: tweet.split())
    words = get_dictionary()
    for tweet in x:
        for j, word in enumerate(tweet):
            if word in words.keys():
                tweet[j] = words[word]
            else:
                tweet[j] = 0
    return pad_sequences(x, maxlen=max_tweet_len), max_tweet_len


def prepare_labels(y):
    positive = 4
    for i, label in enumerate(y):
        if label == positive:
            y[i] = 1
    return np.array(y)


def create_model_binary(max_tweet_len):
    model = Sequential()
    model.add(Embedding(65001, max_tweet_len))
    model.add(SimpleRNN(8))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(
        loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]
    )  # noqa
    return model


def plot_data(history, metric):
    data = pd.DataFrame()
    data["epoch"] = range(3)
    data[metric] = history[metric]
    data["val_" + metric] = history["val_" + metric]
    sns.set(style="darkgrid")
    sns.lineplot(
        x="epoch", y="value", hue="variable", data=pd.melt(data, ["epoch"])
    )  # noqa


path = "../Data/prepared_data.csv"
x, y = open_file(path)
x, max_tweet_len = preapare_tweets(x)
y = prepare_labels(y.values)

x_test = x[:90000]
y_test = y[:90000]

x_train = x[90000:]
y_train = y[90000:]

model = create_model_binary(max_tweet_len)

history = model.fit(
    x_train, y_train, epochs=3, batch_size=512, validation_data=(x_test, y_test)  # noqa
)

plot_data(history.history, metric="accuracy")

plot_data(history.history, metric="loss")

model.save(r"../SimpleRNN_batch_size_128.h5")
