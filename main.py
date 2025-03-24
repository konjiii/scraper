#!/bin/env python3

import csv
import sys
from urllib.parse import (
    quote,
    urlparse,
)  # to sanitize url

import requests
from bs4 import BeautifulSoup

import get_attr
from helper import get_arxiv_doi

QUERY = "AutoML for Earth Observation"
DBLP_URL = "https://dblp.org/search?q="
CROSSREF_URL = "https://api.crossref.org/works/"
PAGES = 10


def write_csv(papers: list[dict[str, str | list[str]]]) -> None:
    with open("papers.csv", "w", encoding="utf-8") as csv_file:
        fieldnames = ["title", "authors", "date", "paper_type", "doi", "publisher", "funders", "link", "pdf"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers:
            # [title, authors, date, paper_type, doi, publisher, funders, link, pdf]
            writer.writerow(paper)


def get_papers(papers: list[dict[str, str | list[str]]], soup: BeautifulSoup) -> None:
    for div in soup.find_all("div", {"class": "gs_r gs_or gs_scl"}):
        form = div.find("span", {"class": "gs_ct1"})
        if form is not None and form.get_text() == "[CITATION]":
            continue

        title = get_attr.get_title(div)
        link = get_attr.get_link(div)
        pdf = get_attr.get_pdf(div)
        authors = ""
        date = ""
        paper_type = ""
        doi = ""
        publisher = ""
        funders = ""

        doi_code = get_doi(title)
        if doi_code is not None:
            # if a doi was found get more metadata from the crossref api

            response = requests.get(CROSSREF_URL + doi_code)

            if response.status_code == 404:
                print("doi not found in crossref", file=sys.stderr)
                with open("failed.doi", "a") as file:
                    file.write(doi_code)
            else:
                with open("success.doi", "a") as file:
                    file.write(doi_code + "\n")
                json = response.json()

                title = get_attr.get_title_new(json)
                authors = get_attr.get_authors(json)
                date = get_attr.get_date(json)
                paper_type = get_attr.get_paper_type(json)
                doi = get_attr.get_doi_url(json)
                publisher = get_attr.get_publisher(json)
                funders = get_attr.get_funders(json)

        papers.append(
            {
                "title": title,
                "authors": authors,
                "date": date,
                "paper_type": paper_type,
                "doi": doi,
                "publisher": publisher,
                "funders": funders,
                "link": link,
                "pdf": pdf,
            }
        )


def get_doi(title: str) -> None | str:
    # find the doi code for the title of a certain paper
    dblp_query = quote(title)

    dblp = DBLP_URL + dblp_query

    response = requests.get(dblp)
    soup = BeautifulSoup(response.content, features="html.parser")

    matches = soup.find("p", {"id": "completesearch-info-matches"})
    if matches is None:
        print("failed to search dblp", file=sys.stderr)
        return None

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

        print(soup.prettify())
        
        get_papers(papers, soup)

    write_csv(papers)


if __name__ == "__main__":
    main()
