import requests
from bs4 import BeautifulSoup


def get_arxiv_doi(doi: str) -> None | str:
    new_doi = None
    arxiv_url = "https://arxiv.org/abs/" + doi.split("arXiv.")[-1]

    response = requests.get(arxiv_url)
    soup = BeautifulSoup(response.content, features="html.parser")

    doi_cell = soup.find("td", {"class": "tablecell doi"})
    if doi_cell is not None:
        new_doi = doi_cell.find("a")["data-doi"]

    return new_doi
