<script lang="ts">
  import jsonData from "../data/papers.json";
  import * as d3 from "d3";
  import { StopwordsEn, StemmerEn } from "@nlpjs/lang-en";
  import { onMount } from "svelte";

  const id = "CooperationGraph";
  // SVG dimensions
  const margin = { top: 20, right: 20, bottom: 50, left: 20 };
  const width = 800 - margin.left - margin.right;
  const height = 800 - margin.top - margin.bottom;

  onMount(() => {
    var svg = d3
      .select(`#${id}`)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.json(
      "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_network.json",
      function (data) {
        // Initialize the links
        var link = svg
          .selectAll("line")
          .data(data.links)
          .enter()
          .append("line")
          .style("stroke", "#aaa");

        // Initialize the nodes
        var node = svg
          .selectAll("circle")
          .data(data.nodes)
          .enter()
          .append("circle")
          .attr("r", 20)
          .style("fill", "#69b3a2");

        // Let's list the force we wanna apply on the network
        var simulation = d3
          .forceSimulation(data.nodes) // Force algorithm is applied to data.nodes
          .force(
            "link",
            d3
              .forceLink() // This force provides links between nodes
              .id(function (d) {
                return d.id;
              }) // This provide  the id of a node
              .links(data.links), // and this the list of links
          )
          .force("charge", d3.forceManyBody().strength(-400)) // This adds repulsion between nodes. Play with the -400 for the repulsion strength
          .force("center", d3.forceCenter(width / 2, height / 2)) // This force attracts nodes to the center of the svg area
          .on("end", ticked);

        // This function is run at each iteration of the force algorithm, updating the nodes position.
        function ticked() {
          link
            .attr("x1", function (d) {
              return d.source.x;
            })
            .attr("y1", function (d) {
              return d.source.y;
            })
            .attr("x2", function (d) {
              return d.target.x;
            })
            .attr("y2", function (d) {
              return d.target.y;
            });

          node
            .attr("cx", function (d) {
              return d.x + 6;
            })
            .attr("cy", function (d) {
              return d.y - 6;
            });
        }
      },
    );
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
