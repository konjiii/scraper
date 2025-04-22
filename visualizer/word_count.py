import csv
import math
from collections import Counter

from bokeh.plotting import figure, show
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

download("punkt_tab")
download("wordnet")
download("stopwords")
LEMMATIZER = WordNetLemmatizer()
STOPWORDS = stopwords.words("english")
PUNCTUATIONS = [".", ",", ":", ";", "'", '"']


def main():
    fieldnames = [
        "title",
        "authors",
        "date",
        "paper_type",
        "doi",
        "publisher",
        "funders",
        "link",
    ]

    papers = list()

    with open("papers.csv", "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            papers.append(row)

    titles = get_field(papers, "title")

    word_counter = Counter()

    for title in titles:
        for word in word_tokenize(title):
            word_counter.update(
                [LEMMATIZER.lemmatize(part.lower()) for part in word.split("-")]
            )

    toremove = list()
    for word, count in word_counter.items():
        if word in STOPWORDS or word in PUNCTUATIONS:
            toremove.append(word)
        elif count < 3:
            toremove.append(word)

    for word in toremove:
        word_counter.pop(word)

    visualize(word_counter)


def visualize(counts: Counter) -> None:
    labels = list(counts.keys())
    labels.sort(key=lambda word: counts[word], reverse=True)
    values = [counts[label] for label in labels]

    p = figure(
        title="publishers of AutoML for EO papers",
        x_axis_label="publisher",
        y_axis_label="amount",
        x_range=labels,
    )

    p.vbar(x=labels, top=values)

    p.xaxis.major_label_orientation = math.pi / 2

    show(p)


def get_field(papers: list[dict[str, str]], name: str) -> list[str]:
    # exclude papers without a known publisher
    return [paper[name] for paper in papers if paper[name] != ""]


if __name__ == "__main__":
    main()
