<script lang="ts">
  import jsonData from "../data/papers.json";
  import * as d3 from "d3";
  import { StopwordsEn, StemmerEn } from "@nlpjs/lang-en";
  import { onMount } from "svelte";

  const id = "CooperationGraph";
  // SVG dimensions
  const margin = { top: 20, right: 20, bottom: 20, left: 20 };
  const width = 1600 - margin.left - margin.right;
  const height = 800 - margin.top - margin.bottom;

  const authors = jsonData.map((item) => item["authors"]);

  interface Node {
    id: string;
    count: number;
  }

  interface Link {
    source: string;
    target: string;
  }

  interface Graph {
    nodes: Node[];
    links: Link[];
  }

  function updateNodes(nodes: Node[], id: string) {
    nodes.forEach((item, idx, arr) => {
      if (item.id == id) {
        arr[idx].count++;
        return;
      }
    });

    const newNode: Node = { id: id, count: 1 };
    nodes.push(newNode);
  }

  function updateLinks(links: Link[], author: string, authors: string[]) {
    authors.forEach((name) => {
      if (name == author) {
        return;
      }

      for (let i = 0; i < links.length; i++) {
        if (links[i].source == author && links[i].target == name) {
          return;
        }
      }
      const newLink: Link = { source: author, target: name };
      links.push(newLink);
    });
  }

  const graph: Graph = { nodes: [], links: [] };
  authors.forEach((item) => {
    item.forEach((name) => {
      updateNodes(graph.nodes, name);
      updateLinks(graph.links, name, item);
    });
  });

  onMount(() => {
    const color = d3.scaleOrdinal(d3.schemeCategory10);
    const nodes = graph.nodes.map((d) => ({ ...d }));
    const links = graph.links.map((d) => ({ ...d }));

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3.forceLink(links).id((d) => d.id),
      )
      .force("charge", d3.forceManyBody())
      .force("x", d3.forceX())
      .force("y", d3.forceY());

    const svg = d3
      .select(`#${id}`)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      .attr("style", "max-width: 100%; height: auto;")
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    const link = svg
      .append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", 2);

    const node = svg
      .append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", 5)
      .attr("fill", (d) => color(d.count));

    simulation.on("tick", () => {
      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
    });
  });
</script>

<div>
  <p>Cooperation graph between authors</p>
  <svg
    {id}
    width={width + margin.left + margin.right}
    height={height + margin.top + margin.bottom}
  >
  </svg>
</div>
