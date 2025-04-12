#!/bin/env python3

import csv
import sys
from pprint import pprint
from urllib.parse import (
    quote,
)  # to sanitize url

import requests
from bs4 import BeautifulSoup
from crossref_commons.iteration import iterate_publications_as_json
from crossref_commons.retrieval import get_publication_as_json

import get_attr

QUERY = "AutoML for Earth Observation"
DBLP_URL = "https://dblp.org/search?q="
CROSSREF_URL = "https://api.crossref.org/works/"
CROSSREF_METADATA_URL = "https://search.crossref.org/search/"
PAGES = 10


def write_csv(papers: list[dict[str, str | list[str]]]) -> None:
    with open("papers.csv", "w", encoding="utf-8") as csv_file:
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
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers:
            # [title, authors, date, paper_type, doi, publisher, funders, link, pdf]
            writer.writerow(paper)


def get_papers(papers: list[dict[str, str | list[str]]], soup: BeautifulSoup) -> None:
    for div in soup.find_all("div", {"class": "gs_r gs_or gs_scl"}):
        # form = div.find("span", {"class": "gs_ct1"})

        title = get_attr.get_title(div)
        if title == "unavailable":
            continue
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
                json = get_publication_as_json(doi_code)

                print("################")
                pprint(json)

                try:
                    title = get_attr.get_title_new(json)
                    authors = get_attr.get_authors(json)
                    date = get_attr.get_date(json)
                    paper_type = get_attr.get_paper_type(json)
                    doi = get_attr.get_doi_url(json)
                    publisher = get_attr.get_publisher(json)
                    funders = get_attr.get_funders(json)
                    print("################")
                    print("ATTRIBUTES")
                    print(title)
                    print(authors)
                    print(date)
                    print(paper_type)
                    print(doi)
                    print(publisher)
                    print(funders)
                except Exception as e:
                    print(f"Failed to get attributes: {e}")
                    continue

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
    queries = {"query.title": title}
    # get doi of first result
    doi = next(iterate_publications_as_json(max_results=189, queries=queries))["DOI"]

    return doi


def main() -> None:
    papers = list()

    for begin in range(0, 10 * PAGES, 10):
        scholar = f"https://scholar.google.com/scholar?start={begin}&q={quote(QUERY)}&hl=en&as_sdt=0,5"

        response = requests.get(scholar)

        print(response.status_code)

        soup = BeautifulSoup(response.content, features="html.parser")

        get_papers(papers, soup)

    write_csv(papers)


if __name__ == "__main__":
    main()
