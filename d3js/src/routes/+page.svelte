<script lang="ts">
  import { Pagination, PaginationItem } from "flowbite-svelte";
  import { ArrowLeftOutline, ArrowRightOutline } from "flowbite-svelte-icons";
  import WordCountChart from "../components/WordCountChart.svelte";
  import CooperationChart from "../components/CooperationChart.svelte";

  let currentChart = 0;

  const charts = [
    { component: WordCountChart, title: "Scatter Plot" },
    { component: CooperationChart, title: "Cooperation Chart" },
  ];

  const previous = () => {
    currentChart = (currentChart - 1 + charts.length) % charts.length;
  };

  const next = () => {
    currentChart = (currentChart + 1) % charts.length;
  };
</script>

<div>
  <h1>Earthquakes</h1>
  <p>
    The data used below includes only earthquakes with a magnitude of 5 or more
    that occurred in 2021.
  </p>

  <h2>Scatter plot</h2>
  <div class="flex justify-center">
    <svelte:component this={charts[currentChart].component} />
  </div>
  <div class="flex justify-center">
    <PaginationItem size="large" class="flex items-center" onclick={previous}>
      <ArrowLeftOutline class="me-2 h-5 w-5" />
      Previous
    </PaginationItem>
    <PaginationItem size="large" class="flex items-center" onclick={next}>
      Next
      <ArrowRightOutline class="ms-2 h-5 w-5" />
    </PaginationItem>
  </div>
</div>
