import re
from functools import reduce

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def delete_names(tweet):
    return re.sub(r"@[A-Za-z0-9]+", "", tweet)


def delete_urls(tweet):
    return re.sub(r"https?://[^\s>]+", "", tweet)


def delete_numbers(tweet):
    return re.sub(r"\d+", "", tweet)


def delete_punctuation(tweet):
    return re.sub(r"[^0-9A-Za-z \t]", "", tweet)


def normalization(data):
    data = data.str.lower()
    data = data.apply(lambda tweet: delete_names(tweet))
    data = data.apply(lambda tweet: delete_urls(tweet))
    data = data.apply(lambda tweet: delete_numbers(tweet))
    data = data.apply(lambda tweet: delete_punctuation(tweet))
    return data


def delete_stop_words(data):
    stop_words = stopwords.words("english")
    return data.apply(lambda tweet: [word for word in tweet if word not in stop_words])


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


def clean_data(tweet):
    processing_steps = [
        normalization,
        tokenization,
        delete_stop_words,
        remove_repeated_letters,
        lemmatizaton,
    ]
    return reduce(lambda acc, fun: fun(acc), processing_steps, tweet)
