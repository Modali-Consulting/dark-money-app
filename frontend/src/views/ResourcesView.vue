<template>
  <div>
    <h1>Resource Directory</h1>
    <div class="grid grid-2">
      <div class="card">
        <h3>Filters</h3>
        <label>Category</label>
        <select>
          <option>All</option>
          <option>Federal Campaign Finance</option>
          <option>Political Ads</option>
        </select>
        <label>Jurisdiction</label>
        <select>
          <option>All</option>
          <option>US</option>
          <option>Global</option>
        </select>
      </div>
      <div class="card">
        <h3>Resources for Tracking Dark Money</h3>
        <p class="badge">15+ seeded sources</p>
        <ul>
          <li>OpenSecrets</li>
          <li>FEC Disbursements</li>
          <li>IRS Exempt Orgs</li>
          <li>Meta Ad Library</li>
        </ul>
      </div>
    </div>
    <div class="card">
      <div class="topbar">
        <h3>Dark Money Resource Map</h3>
        <label>
          <input type="checkbox" v-model="interactive" />
          Recreate as interactive graph
        </label>
      </div>
      <div v-if="!interactive">
        <img src="/diagrams/dark-money-resources.svg" alt="Dark money resources diagram" style="width:100%; border-radius:12px;" />
      </div>
      <div v-else>
        <p>Interactive graph preview (placeholder). Connect nodes by category, source type, and jurisdiction.</p>
        <div class="card">
          <strong>Federal Finance</strong> → OpenSecrets → Donor Lookup
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const interactive = ref(false);
</script>
