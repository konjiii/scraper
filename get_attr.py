def get_pdf(div) -> str:
    pdf_div = div.find("div", {"class": "gs_or_ggsm"})
    if pdf_div is None or pdf_div.a.span.get_text() != "[PDF]":
        return "unavailable"

    return pdf_div.a["href"]


def get_link(div) -> str:
    try:
        return div.h3.a["href"]
    except Exception as _:
        return "unavailable"


def get_title(div) -> str:
    try:
        return div.h3.a.get_text()
    except Exception as _:
        return "unavailable"


def get_title_new(json) -> str:
    title = json["message"]["title"][0]
    return title


def get_doi_url(json) -> str:
    doi_url = "https://doi.org/" + json["message"]["DOI"]
    return doi_url


def get_date(json) -> str:
    date = json["message"]["indexed"]["date-time"]
    return date


def get_publisher(json) -> str:
    publisher = json["message"]["publisher"]
    return publisher


def get_paper_type(json) -> str:
    paper_type = json["message"]["type"]
    return paper_type


def get_funders(json) -> list[str]:
    if "funder" in json["message"].keys():
        funders = [funder["name"] for funder in json["message"]["funder"]]
        return funders
    else:
        return ["unavailable"]


def get_authors(json) -> list[str]:
    authors = [
        f"{author['given'] if 'given' in author.keys() else ''} {author['family']}"
        for author in json["message"]["author"]
    ]
    return authors
