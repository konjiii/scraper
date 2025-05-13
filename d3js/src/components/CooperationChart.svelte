<script lang="ts">
  import jsonData from "../data/papers.json";
  import * as d3 from "d3";
  import { StopwordsEn, StemmerEn } from "@nlpjs/lang-en";
  import { onMount } from "svelte";

  const id = "wordCount";
  const stemmer = new StemmerEn();
  stemmer.stopwords = new StopwordsEn();
  const data: Map<String, number> = new Map();
  // SVG dimensions
  const margin = { top: 20, right: 20, bottom: 50, left: 20 };
  const width = 800 - margin.left - margin.right;
  const height = 800 - margin.top - margin.bottom;

  jsonData.forEach((item) => {
    const title = item["title"];

    // normalize, tokenize, stem, and remove stopwords
    const words: String[] = stemmer.tokenizeAndStem(title, false);

    words.forEach((word) => {
      data.set(word, (data.get(word) || 0) + 1);
    });
  });

  // get sorted list of word count pairs with count above 4
  const top = [...data.entries()]
    .sort((a, b) => b[1] - a[1])
    .filter((entry) => entry[1] >= 5);

  // split words and counts into two arrays
  const words = top.map((entry) => entry[0]);

  onMount(() => {
    const svg = d3
      .select(`#${id}`)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // x axis
    const xAxis = d3.scaleBand().domain(words).range([0, width]).padding(0.2);
    svg
      .append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(xAxis))
      .selectAll("text")
      .style("text-anchor", "start")
      .attr("dx", "5")
      .attr("dy", "5")
      .attr("transform", "rotate(45)");

    // x label

    // y axis
    const yAxis = d3.scaleLinear().domain([0, 30]).range([height, 0]);
    svg.append("g").call(d3.axisLeft(yAxis));

    // bars
    svg
      .selectAll(".bar")
      .data(words)
      .enter()
      .append("rect")
      .attr("x", (word: string) => xAxis(word))
      .attr("y", (word: string) => yAxis(data.get(word)))
      .attr("width", xAxis.bandwidth())
      .attr("height", (word: string) => height - yAxis(data.get(word)))
      .attr("fill", "steelblue");
  });
</script>

<div>
  <p>Word count</p>
  <svg
    {id}
    width={width + margin.left + margin.right}
    height={height + margin.top + margin.bottom}
  >
  </svg>
</div>
