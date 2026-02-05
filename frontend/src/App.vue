<template>
  <div class="app-shell">
    <aside class="sidebar">
      <h2>DarkMoney Lens</h2>
      <nav>
        <router-link to="/">Dashboard</router-link>
        <router-link to="/resources">Resources</router-link>
        <router-link to="/cases">Cases</router-link>
        <router-link to="/entities">Entities</router-link>
        <router-link to="/powermap">Power Map</router-link>
        <router-link to="/pipelines">Pipelines</router-link>
        <router-link to="/observability">Observability</router-link>
        <router-link to="/settings">Settings</router-link>
      </nav>
    </aside>
    <main class="main">
      <div class="topbar">
        <input placeholder="Search across entities, cases, evidence..." />
        <router-link to="/auth/login">Login</router-link>
      </div>
      <router-view />
    </main>
  </div>
</template>
