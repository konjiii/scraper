import csv
import math
from collections import Counter

from bokeh.plotting import figure, show


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
        "pdf",
    ]

    papers = list()

    with open("papers.csv", "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            papers.append(row)

    authors = get_field(papers, "authors")

    authors = [person for paper in authors for person in eval(paper)]

    author_counter = Counter(authors)

    visualize(author_counter)


def visualize(counts: Counter) -> None:
    labels = list(counts.keys())
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
