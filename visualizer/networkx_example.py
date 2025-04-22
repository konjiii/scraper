import csv

import networkx as nx


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

    authors = get_field(papers, "authors")

    for idx in range(len(authors)):
        while " " in authors[idx]:
            authors[idx].remove(" ")

    if [] in authors:
        authors.remove([])

    visualize(authors)


def visualize(authors: list[list[str]]) -> None:
    # all_authors = list(set([person for lst in authors for person in lst]))
    # author_ids = {name: idx for idx, name in enumerate(all_authors)}

    adjacency_dict = dict()
    for idx, lst in enumerate(authors):
        # if idx > 10:
        #     break
        for name in lst:
            adjacency_dict.setdefault(name, list())
            for name2 in lst:
                if name == name2 or name2 in adjacency_dict[name]:
                    continue
                adjacency_dict[name].append(name2)

    G = nx.Graph(adjacency_dict)

    nx.write_gexf(G, "graph.gexf")

    # nx.draw_shell(G, nlist=authors[:11], with_labels=True)
    # nx.draw_networkx(G, with_labels=True)
    #
    # plt.show()


def get_field(papers: list[dict[str, str]], name: str) -> list[list[str]]:
    # exclude papers without a known publisher
    return [eval(paper[name]) for paper in papers if paper[name] != ""]


if __name__ == "__main__":
    main()
