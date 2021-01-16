import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def normalization(data):
    data = data.str.lower()
    data = data.apply(lambda tweet: re.sub(r"@[A-Za-z0-9]+", "", tweet))
    data = data.apply(
        lambda tweet: re.sub(r"https?://[^\s>]+", "", tweet)
    )  # delete url
    data = data.apply(lambda tweet: re.sub(r"\d+", "", tweet))
    data = data.apply(
        lambda tweet: re.sub(r"[^0-9A-Za-z \t]", "", tweet)
    )  # delete punctuation
    return data  # noqa


def delete_stop_words(data):
    stop_words = stopwords.words("english")
    return data.apply(
        lambda tweet: [word for word in tweet if word not in (stop_words)]
    )


def tokenization(data):
    return data.apply(lambda tweet: tweet.split())


def remove_repeated_letters(data):
    pattern = re.compile(r"(.)\1{2,}")
    return data.apply(
        lambda tweet: [pattern.sub(r"\1\1", word) for word in tweet]
    )  # noqa


def lemmatizaton(data):
    lemmatizer = WordNetLemmatizer()
    return data.apply(
        lambda tweet: [lemmatizer.lemmatize(word) for word in tweet]
    )  # noqa


def clean_data(x):
    x = normalization(x)
    x = tokenization(x)
    x = delete_stop_words(x)
    x = remove_repeated_letters(x)
    return lemmatizaton(x)
