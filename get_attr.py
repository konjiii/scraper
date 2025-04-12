def get_pdf(div) -> str:
    pdf_div = div.find("div", {"class": "gs_ctg2"})

    if pdf_div is None:
        return "unavailable"

    if pdf_div.a.span.get_text() is not None and pdf_div.a.span.get_text() == "[PDF]":
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
    return json["title"][0]


def get_doi_url(json) -> str:
    return "https://doi.org/" + json["DOI"]


def get_date(json) -> str:
    date_parts = json["published"]["date-parts"][0]
    date = ""
    for part in date_parts:
        date += f"-{part}"
    return date[1:]


def get_publisher(json) -> str:
    return json["publisher"]


def get_paper_type(json) -> str:
    return json["type"]


def get_funders(json) -> list[str]:
    if "funder" in json.keys():
        funders = [funder["name"] for funder in json["funder"]]
        return funders
    else:
        return ["unavailable"]


def get_authors(json) -> list[str]:
    authors = [
        f"{author['given'] if 'given' in author.keys() else ''} {author['family']}"
        for author in json["author"]
    ]
    return authors
