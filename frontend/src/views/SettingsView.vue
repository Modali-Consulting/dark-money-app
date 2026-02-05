<template>
  <div>
    <h1>Settings</h1>
    <div class="card">
      <h3>Manage Sources</h3>
      <table class="table">
        <thead>
          <tr>
            <th>Source</th>
            <th>Enabled</th>
            <th>Schedule</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>demo_resources</td>
            <td><span class="badge success">Enabled</span></td>
            <td>@daily</td>
          </tr>
          <tr>
            <td>demo_finance</td>
            <td><span class="badge warn">Paused</span></td>
            <td>@hourly</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
