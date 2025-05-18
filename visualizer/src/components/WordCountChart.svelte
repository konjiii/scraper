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
  const margin = { top: 20, right: 20, bottom: 50, left: 50 };
  const width = 1600 - margin.left - margin.right;
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
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // x axis
    const x = d3.scaleBand().domain(words).range([0, width]).padding(0.2);
    const xAxis = d3.axisBottom(x);
    svg
      .append("g")
      .attr("transform", `translate(0,${height})`)
      .call(xAxis)
      .selectAll("text");

    // x label
    svg
      .append("text")
      .attr("text-anchor", "middle")
      .attr("x", width / 2)
      .attr("y", height + margin.bottom - 10)
      .text("Words");

    // y label
    svg
      .append("text")
      .attr("text-anchor", "middle")
      .attr("transform", `rotate(-90)`)
      .attr("x", -height / 2)
      .attr("y", -margin.left + 20) // shift away from y-axis a bit
      .text("Counts");

    // y axis
    const y = d3.scaleLinear().domain([0, 30]).range([height, 0]);
    const yAxis = d3.axisLeft(y);
    svg.append("g").call(yAxis);

    // bars
    svg
      .selectAll(".bar")
      .data(words)
      .enter()
      .append("rect")
      .attr("x", (word: string) => x(word))
      .attr("y", (word: string) => y(data.get(word)))
      .attr("width", x.bandwidth())
      .attr("height", (word: string) => height - y(data.get(word)))
      .attr("fill", "steelblue");
  });
</script>

<div>
  <p>Word count</p>
  <svg {id}> </svg>
</div>
