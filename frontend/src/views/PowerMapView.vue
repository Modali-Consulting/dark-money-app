<template>
  <div>
    <h1>Global Power Map</h1>
    <div class="grid grid-2">
      <div class="card">
        <h3>Graph Editor</h3>
        <p>Drag nodes to build relationships (placeholder).</p>
        <div class="card">
          Liberty Advocates Network → Citizens for Progress PAC
        </div>
      </div>
      <div class="card">
        <h3>Import / Export JSON</h3>
        <textarea rows="10" placeholder="Paste graph JSON"></textarea>
        <div style="display:flex; gap:8px; margin-top:8px;">
          <button>Import</button>
          <button class="secondary">Export</button>
        </div>
      </div>
    </div>
  </div>
</template>
