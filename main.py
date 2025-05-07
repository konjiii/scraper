#!/bin/env python3

import csv

# official crossref api
from crossref_commons.iteration import iterate_publications_as_json
from crossref_commons.retrieval import get_publication_as_json

# unofficial google scholar api
from scholarly import scholarly
from tqdm import tqdm

import get_attr
from helper import clean_title

QUERY = '("Automated Machine Learning" OR "Neural Architecture Search") AND "Earth Observation"'
DBLP_URL = "https://dblp.org/search?q="
CROSSREF_URL = "https://api.crossref.org/works/"
CROSSREF_METADATA_URL = "https://search.crossref.org/search/"
PAPERS = 100


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
            "abstract",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers:
            # [title, authors, date, paper_type, doi, publisher, funders, link, pdf]
            writer.writerow(paper)


def get_papers() -> list[dict[str, str | list[str]]]:
    papers = list()
    dois = list()

    results = scholarly.search_pubs(QUERY)

    for i, result in tqdm(enumerate(results), desc="Finding papers...", total=PAPERS):
        if i > PAPERS:
            break

        if "bib" not in result.keys() or "title" not in result["bib"].keys():
            print("missing title:")
            print(result)
            continue

        title = result["bib"]["title"]
        if "pub_url" not in result.keys():
            print("missing url:")
            print(result)
            continue

        link = result["pub_url"]
        authors = ""
        date = ""
        paper_type = ""
        doi = ""
        publisher = ""
        funders = ""

        doi_code = get_doi(title)
        if doi_code is None:
            print("doi not found")
            continue

        if doi_code in dois:
            print(f"duplicate paper: {title}")
            continue

        dois.append(doi_code)
        # if a doi was found get more metadata from the crossref api
        json = get_publication_as_json(doi_code)
        # print("################")
        # pprint(json)
        try:
            title_old = title
            title = get_attr.get_title_new(json)

            title_old_clean = clean_title(title_old)
            title_clean = clean_title(title)
            print(title_old_clean)
            print(title_clean)

            # find cutoff point of google scholar title
            cutoff = None
            if "…" in title_old_clean:
                cutoff = title_old_clean.find("…")
            if (
                title_clean[:cutoff] not in title_old_clean[:cutoff]
                and title_old_clean[:cutoff] not in title_clean[:cutoff]
            ):
                print("title not the same:")
                print(title_old)
                print(title)
                continue

            authors = get_attr.get_authors(json)
            date = get_attr.get_date(json)
            paper_type = get_attr.get_paper_type(json)
            doi = get_attr.get_doi_url(json)
            publisher = get_attr.get_publisher(json)
            funders = get_attr.get_funders(json)
            abstract = get_attr.get_abstract(json)
            # print("################")
            # print("ATTRIBUTES")
            # print(title)
            # print(authors)
            # print(date)
            # print(paper_type)
            # print(doi)
            # print(publisher)
            # print(funders)
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
                "abstract": abstract,
            }
        )

    return papers


def get_doi(title: str) -> None | str:
    # find the doi code for the title of a certain paper
    queries = {"query.title": title}
    # get doi of first result
    doi = next(iterate_publications_as_json(max_results=189, queries=queries))["DOI"]

    return doi


def main() -> None:
    papers = get_papers()

    write_csv(papers)


if __name__ == "__main__":
    main()
