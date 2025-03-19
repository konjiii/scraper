#!/bin/env python3

import csv
import sys
from urllib.parse import (
    quote,
    urlparse,
)  # to sanitize url

import requests
from bs4 import BeautifulSoup

from get_attr import get_link, get_pdf, get_title
from helper import get_arxiv_doi

QUERY = "AutoML for Earth Observation"
DBLP_URL = "https://dblp.org/search?q="
CROSSREF_URL = "https://api.crossref.org/works/"
PAGES = 10


def write_csv(papers: list[list[str]]) -> None:
    with open("papers.csv", "w") as csv_file:
        fieldnames = ["title", "link", "pdf"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers:
            writer.writerow({"title": paper[0], "link": paper[1], "pdf": paper[2]})


def get_papers(papers: list[list[str]], soup: BeautifulSoup) -> None:
    for div in soup.find_all("div", {"class": "gs_r gs_or gs_scl"}):
        form = div.find("span", {"class": "gs_ct1"})
        if form is not None and form.get_text() == "[CITATION]":
            continue

        title = get_title(div)
        link = get_link(div)
        pdf = get_pdf(div)

        doi_code = get_doi(title)
        if doi_code is not None:
            # if a doi was found get more metadata from the crossref api
            print(title)
            print(doi_code)

            response = requests.get(CROSSREF_URL + doi_code)

            if response.status_code == 404:
                print("doi not found in crossref", file=sys.stderr)
                with open("failed.doi", "a") as file:
                    file.write(doi_code)
            else:
                with open("success.doi", "a") as file:
                    file.write(doi_code + "\n")
                print(response.json())

        papers.append([title, link, pdf])


def get_doi(title: str) -> None | str:
    # find the doi code for the title of a certain paper
    dblp_query = quote(title)

    dblp = DBLP_URL + dblp_query

    response = requests.get(dblp)
    soup = BeautifulSoup(response.content, features="html.parser")

    matches = soup.find("p", {"id": "completesearch-info-matches"})
    if matches is None:
        print("failed to search dblp", file=sys.stderr)

    if matches.text == "no matches":
        return None

    paper_list = soup.find("ul", {"class": "publ-list"})

    doi = None
    parsed_doi = None

    for list_item in paper_list.find_all("li", recursive=False):
        if list_item["class"][0] == "year":
            continue

        doi = list_item.find("li", {"class": "drop-down"}).find("a")["href"]

        parsed_url = urlparse(doi)
        if parsed_url.netloc != "doi.org":
            continue

        parsed_doi = parsed_url.path[1:].replace("/", "%2F")

        if "arXiv" in parsed_doi:
            old_doi = parsed_doi

            parsed_doi = get_arxiv_doi(parsed_doi)
            if parsed_doi is None:
                with open("failed.doi", "a") as file:
                    file.write(old_doi + "\n")

        break

    return parsed_doi


def main() -> None:
    papers = list()

    for begin in range(0, 10 * PAGES, 10):
        scholar = f"https://scholar.google.com/scholar?start={begin}&q={quote(QUERY)}&hl=en&as_sdt=0,5"

        response = requests.get(scholar)

        soup = BeautifulSoup(response.content, features="html.parser")

        get_papers(papers, soup)

    write_csv(papers)


if __name__ == "__main__":
    main()
