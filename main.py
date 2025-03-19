#!/bin/env python3

import csv

import requests
from bs4 import BeautifulSoup
from requests.models import Response

search: str = "AutoML for Earth Observation"
pages: int = 1
papers: list[list[str]] = list()


def get_pdf(div) -> str:
    pdf_div = div.find("div", {"class": "gs_or_ggsm"})
    if pdf_div is None or pdf_div.a.span.get_text() != "[PDF]":
        return "not available"

    return pdf_div.a["href"]


def get_link(div) -> str:
    return div.h3.a["href"]


def get_title(div) -> str:
    return div.h3.a.get_text()


def write_csv(papers: list[list[str]]) -> None:
    with open("papers.csv", "w") as csv_file:
        fieldnames = ["title", "link", "pdf"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers:
            writer.writerow({"title": paper[0], "link": paper[1], "pdf": paper[2]})


def get_papers(soup: BeautifulSoup) -> None:
    for div in soup.find_all("div", {"class": "gs_r gs_or gs_scl"}):
        form = div.find("span", {"class": "gs_ct1"})
        if form is not None and form.get_text() == "[CITAAT]":
            continue

        title: str = get_title(div)
        link: str = get_link(div)
        pdf: str = get_pdf(div)

        papers.append([title, link, pdf])


def main() -> None:
    for begin in range(0, 10 * pages, 10):
        url: str = f"https://scholar.google.com/scholar?start={begin}&q={search.replace(' ', '+')}&hl=nl&as_sdt=0,5"

        response: Response = requests.get(url)

        soup: BeautifulSoup = BeautifulSoup(response.content, features="html.parser")

        get_papers(soup)

    write_csv(papers)


if __name__ == "__main__":
    main()
