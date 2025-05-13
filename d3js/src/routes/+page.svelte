<script lang="ts">
  import WordCountChart from "../components/WordCountChart.svelte";
</script>

<div>
  <h1>Earthquakes</h1>
  <p>
    The data used below includes only earthquakes with a magnitude of 5 or more
    that occurred in 2021.
  </p>

  <h2>Scatter plot</h2>
  <div class="flex justify-center">
    <WordCountChart />
  </div>
</div>
