<template>
  <div>
    <h1>Pipelines</h1>
    <div class="grid grid-2">
      <div class="card">
        <h3>Current vs Future State</h3>
        <p><strong>Current:</strong> Scraper → transforms → production tables.</p>
        <p><strong>Future:</strong> Extractor → Bronze → Silver → Gold → Serving.</p>
        <ul>
          <li>Bronze: append-only raw payloads</li>
          <li>Silver: normalized per source</li>
          <li>Gold: canonical entities + relationships</li>
          <li>Serving: UI-optimized projections</li>
        </ul>
      </div>
      <div class="card">
        <h3>Medallion Pipeline Diagram</h3>
        <img src="/diagrams/medallion-pipeline.svg" alt="Medallion architecture" style="width:100%; border-radius:12px;" />
      </div>
    </div>
    <div class="card">
      <h3>Pipeline Runs</h3>
      <table class="table">
        <thead>
          <tr>
            <th>Run</th>
            <th>Source</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>2026-02-01</td>
            <td>demo_resources</td>
            <td><span class="badge success">Success</span></td>
          </tr>
          <tr>
            <td>2026-02-02</td>
            <td>demo_finance</td>
            <td><span class="badge warn">Lagging</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
